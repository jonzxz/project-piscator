<?php

use yii\helpers\Url;
use yii\helpers\Html;
use yii\helpers\ArrayHelper;
use yii\widgets\DetailView;
use yii\bootstrap4\ActiveForm;
use yii\bootstrap4\Accordion;
use yii\grid\GridView;
use yii\data\ActiveDataProvider;
use yii\db\Expression;

use common\models\Bug;
use common\models\User;

use kartik\select2\Select2;
use kartik\widgets\SwitchInput;
use yii\web\JsExpression;

use rmrevin\yii\fontawesome\FAS;
use yii\widgets\ListView;

/**
* @var yii\web\View $this
* @var common\models\Bug $model
*/

$this->title = "#".$model->id." ".$model->title;
$this->params['breadcrumbs'][] = ['label' => 'Bugs', 'url' => ['index']];
$this->params['breadcrumbs'][] = $this->title;

?>

<div class="bug-view">
   <div class="row m-1 mb-2">
      <!-- tag -->
         <div id="tag-badge-wrapper-top" class="ml-3 mr-4 pb-2">
            <?php foreach ($model->tags as $tag) : ?>
               <div id="top-tag-<?= $tag->id ?>" class="py-1 px-2 font-weight-normal text-uppercase badge badge-pill badge-success"><?= $tag->name ?>&nbsp;</div>
            <?php endforeach; ?>
         </div>
   </div>

      <div class="d-flex mr-1 mt-1 justify-content-center" style="margin-left:0.7%;width:98.5%"> <!-- no background cuz covered , this row is for assigned to and status-->
         <div class="col-8 d-flex align-items-start flex-column rounded" style="background:white">
            <span class="h6 pt-2 pl-2">
               Submitted by
               <?php
               echo Html::tag('span', Html::encode(User::findIdentity($model->created_by)->publicIdentity),
               ['class' => 'text-uppercase font-weight-normal badge badge-light']);
               ?>
               on
               <?= Html::tag('span', Html::encode(Yii::$app->formatter->asDateTime($model->created_at)),
               ['class' => 'text-uppercase font-weight-normal badge badge-light']); ?>
            </span>
            <!-- TODO:: show list view for the ticket's lifecycle -->
            <span class="h6 pt-2 pl-2">
               Updated by
               <?= Html::tag('span', Html::encode(User::findIdentity($model->updated_by)->publicIdentity),
               ['class' => 'text-uppercase font-weight-normal badge badge-light', 'id'=>'updated_by']); ?>
               on
               <?= Html::tag('span', Html::encode(Yii::$app->formatter->asDateTime($model->updated_at)),
               ['class' => 'text-uppercase font-weight-normal badge badge-light', 'id'=>'updated_at']); ?>
            </span>
         </div>

         <div class="col-4 d-flex align-items-end flex-column" style="background: white">
            <div class="text-left h-100">
               <div class="h2 pt-2">
                  Status
                  <?php
                  echo Html::tag('span', Html::encode($model->bug_status),
                  ['class' => 'text-uppercase font-weight-normal badge badge-pill '.$model->bugStatusBadgeColor, 'id'=>'bug_status']);
                  ?>
               </div>
               <div class="h5 p-0">
                  Priority
                  <?php
                     echo Html::tag('span', Html::encode($model->priority_level),
                     ['class' => 'badge pl-4 pr-4 badge-pill '.$model->priorityLevelBadgeColor, 'id'=>'priority_level'])
                   ?>
               </div>
               <div class="h5 p-0">
                  Assigned
                  <?php
                     echo Html::tag('span', $model->developer_user_id == null ? "Unassigned" : Html::encode(User::findIdentity($model->developer_user_id)->publicIdentity),
                     ['class' => 'badge badge-light', 'id'=>'developer_user']);
                  ?>
               </div>
             </div>
         </div>
      </div>
      <!-- bug description -->
      <div class="flex-row ml-1 d-flex mr-1 mt-4">
         <div class="col-12 d-flex flex-column">
            <h2>Description</h2>
            <div class="jumbotron bg-white">
               <?php
                  echo $model->description;
                ?>
            </div>
         </div>
      </div>
         <div class='card d-flex' style="background:none">
            <?php if(Yii::$app->user->can(User::ROLE_DEVELOPER) || Yii::$app->user->can(User::ROLE_TRIAGER) || Yii::$app->user->can(User::ROLE_REVIEWER)): ?>
               <div class="col-12">
                  <?php $taskForm = ActiveForm::begin([
                             'id' => 'taskForm',
                             'action' => 'process-interaction?id='.$model->id,
                         ]); ?>
                     <div class="card mt-2">
                        <div class="card-header">
                           <a id="task-form-header" class="btn btn-sm btn-outline-primary" href="#">Update Bug Ticket Status Form</a>
                        </div>
                        <div id="task-form-body">
                           <div class="card-body">
                              <?php echo $taskForm->errorSummary($taskModel); ?>
                              <?php
                                 if (Yii::$app->user->can(User::ROLE_DEVELOPER)){
                                    if(($model->bug_status == Bug::BUG_STATUS_ASSIGNED || $model->bug_status == Bug::BUG_STATUS_REOPEN) && $model->developer_user_id && $model->developer_user_id == Yii::$app->user->id){
                                          echo $taskForm->field($taskModel, 'accept')->widget(SwitchInput::classname(), [
                                              'value' => true,
                                              'pluginOptions' => [
                                                  'size' => 'medium',
                                                  'onColor' => 'success',
                                                  'offColor' => 'danger',
                                                  'onText' => 'Yes',
                                                  'offText' => 'No',
                                              ]
                                          ]);
                                    }
                                    if ($model->bug_status == Bug::BUG_STATUS_FIXING && $model->developer_user_id == Yii::$app->user->id) {
                                       echo $taskForm->field($taskModel, 'status')->dropDownList($taskModel::getStatusDeveloper());
                                    }
                                    echo $taskForm->field($taskModel, 'notes')->textarea(['rows' => 3]);
                                 } elseif (Yii::$app->user->can(User::ROLE_TRIAGER)){
                                    if($model->bug_status == Bug::BUG_STATUS_NEW || $model->bug_status == Bug::BUG_STATUS_REOPEN){
                                       echo $taskForm->field($taskModel, 'developer_user_id')->widget(Select2::classname(), [
                                          'data' => ArrayHelper::map($availableDevelopers, 'id', 'publicIdentity'),
                                          'options' => ['placeholder' => 'Select Developer ...'],
                                          'pluginOptions' => [
                                              'allowClear' => true
                                          ],
                                       ]);
                                       echo $taskForm->field($taskModel, 'status')->dropDownList($taskModel::getStatusTriager());
                                    }
                                    echo $taskForm->field($taskModel, 'priority_level')->dropDownList(Bug::getAllPriorityLevel());
                                    echo $taskForm->field($taskModel, 'notes')->textarea(['rows' => 3]);
                                 } elseif (Yii::$app->user->can(User::ROLE_REVIEWER)){
                                    if($model->bug_status == Bug::BUG_STATUS_PENDING_REVIEW){
                                       echo $taskForm->field($taskModel, 'status')->dropDownList($taskModel::getStatusReviewer());
                                       echo $taskForm->field($taskModel, 'notes')->textarea(['rows' => 3]);
                                    }
                                 }
                              ?>
                           </div>
                           <span class="h5 ml-3 mb-2">Update Tags</span>
                           <div id="tag-wrapper" class="row m-1 mb-2">
                              <div id="tag-badge-wrapper" class="ml-3 mr-4">
                                 <?php foreach ($model->tags as $tag) : ?>
                                    <div id="tag-<?= $tag->id ?>" class="py-1 px-2 font-weight-normal text-uppercase badge badge-pill badge-secondary"><?= $tag->name ?>&nbsp;<a class="delete-tag" data-tagid="<?= $tag->id ?>" href="#"><i class="text-white fas fa-times"></i></a></div>
                                 <?php endforeach; ?>
                              </div>

                              <input id="create-tag-input" type="text" name="create-tag" placeholder="e.g. copywriting">
                              <a id="create-tag" class="btn btn-primary text-white">Create Tag</a>
                           </div>
                           <div class="card-footer">
                               <?php echo Html::submitButton('Update', ['class' => 'btn btn-primary']) ?>
                           </div>
                        </div>

                     </div>
                  <?php ActiveForm::end(); ?>
               </div>
            <?php endif; ?>

      <div class="flex-row ml-1 d-flex mr-1 mt-4">
         <div class="col-12 d-flex flex-column">
           <h2>Attachments</h2>
            <div class="jumbotron bg-white">
                <?= $this->render('_documentUpdate', [ 'model' => $model ]); ?>
            </div>
         </div>
      </div>

      <div class="card m-2">
         <div class="card-header">
            Lifecycle
         </div>
         <div class="card-body">
            <?php foreach ($lifecycle as $action) : ?>
               <div class="lifecycle-row">
                  <span class="badge badge-light"><?= $action->action_type ?></span> on <?= Yii::$app->formatter->asDateTime($action->created_at) ?> by <span class="badge badge-light"><?= User::findOne($action->created_by)->publicIdentity ?> (<?= strtoupper(array_keys(Yii::$app->authManager->getRolesByUser($action->created_by))[0]) ?>)</span>
               </div>
            <?php endforeach; ?>
         </div>
      </div>

      <!-- comment begins here -->
      <div class="flex-row ml-1 mr-1 mt-4 p-1" style="background:none">
            <!-- if no comment do something -->
         <?php
            echo Accordion::widget([
               'items' => [
                  [
                     'label' => 'Comments',
                     'content' => ListView::widget([
                        'dataProvider' => $dataProvider,
                        'itemView' => 'comment',
                        'summary' => '',
                        'viewParams' => [
                           'fullView' => true,
                        ],
                     ]),
                     'contentOptions' => ['class' => 'in']
                  ]
               ],
            ])
          ?>
       </div>
       <div class="flex-row ml-1 mr-1 mt-2 p-1" style="background:none">
         <?php $form = ActiveForm::begin(); ?>
         <?php echo $form->field($comment, 'bug_id')->hiddenInput(['value'=>$model->id])->label(false);?>
         <?php echo $form->field($comment, 'comment')->textArea(['rows'=>6]) ?>
         <?php echo Html::submitButton('Post', ['class'=> 'btn btn-primary'])?>
         <?php ActiveForm::end();?>
      </div>
   </div>
</div>

<?php

$script = <<< JS
   $('#taskForm').on('beforeSubmit', function() {
      var data = $('#taskForm').serialize();
      $.ajax({
         url: $('#taskForm').attr('action'),
         type: 'POST',
         data: data,
         success: function (data) {
            // Implement successful
            console.log(data)
            let success = data.success;
            let model = data.model;
            let errors = data.errors;
            if(success){
               $('#task-form-body').slideUp();
               $('#updated_by').text(model.updated_by);
               $('#updated_at').text(model.updated_at);
               $('#bug_status').removeClass('badge-warning').removeClass('badge-success').removeClass('badge-info').removeClass('badge-light').addClass(model.bug_status_badge).text(model.bug_status);
               $('#priority_level').removeClass('badge-info').removeClass('badge-warning').removeClass('badge-danger').removeClass('badge-light').addClass(model.priority_level_badge).text(model.priority_level);
               $('#developer_user').text(model.developer);
            } else {
               processErrorResponse(errors)
            }
         },
         error: function(jqXHR, errMsg) {
            // alert(errMsg);
            console.log(jqXHR);
            console.log(errMsg);
            alert("Please try again.");
         }
      });
      return false; // prevent default submit
   });

   $('#create-tag').on('click', function(e) {
      console.log(this)
      var new_tag_name = $("#create-tag-input").val()
      var data = {
         "BugTag": {
            "bug_id" : $model->id,
            "name" : new_tag_name
         }
      }
      console.log(data)
      $.ajax({
         url: 'create-tag',
         type: 'POST',
         data: data,
         success: function (data) {
            // Implement successful
            console.log(data)
            let success = data.success;
            let model = data.model;
            let errors = data.errors;
            if(success){
               const tag_id = model.id;
               const tag_name = model.name;

               const html = '<div style="display:none;" id="tag-'+tag_id+'" class="py-1 px-2 font-weight-normal text-uppercase badge badge-pill badge-secondary">'+tag_name+'&nbsp;<a class="delete-tag" data-tagid="'+tag_id+'" href="#"><i class="text-white fas fa-times"></i></a></div>';
               // for tag on top
               const html2 = '<div style="" id="top-tag-'+tag_id+'" class="py-1 px-2 font-weight-normal text-uppercase badge badge-pill badge-success">'+tag_name+'&nbsp;</div>';

               $('#tag-badge-wrapper-top').append(html2);
               $('#top-tag'+tag_id).fadeIn();
               $('#tag-badge-wrapper').append(html);
               $("#create-tag-input").val("");
               $('#tag-'+tag_id).fadeIn();
               $('.delete-tag').off();
               addOnClickEventListenerForDeleteTag();
            } else {
               processErrorResponse(errors);
            }
         },
         error: function(jqXHR, errMsg) {
            // alert(errMsg);
            console.log(jqXHR);
            console.log(errMsg);
            alert("Please try again.");
         }
      });
      return false; // prevent default submit
   });

   addOnClickEventListenerForDeleteTag();
   function addOnClickEventListenerForDeleteTag(){
      $('.delete-tag').on('click', function(e) {
         var data = {
            "id" : $(this).data().tagid
         }
         $.ajax({
            url: 'delete-tag',
            type: 'POST',
            data: data,
            success: function (data) {
               // Implement successful
               console.log(data)
               let success = data.success;
               let model = data.model;
               let errors = data.errors;
               if(success){
                  if(model.delete_status == "disabled"){
                     $('#tag-'+model.id).fadeOut(function(){
                        $('#tag-'+model.id).remove();
                     });
                     $('#top-tag-'+model.id).fadeOut(function() {
                        $('#top-tag-'+model.id).remove();
                     })
                  } else {
                     alert("Failed to delete");
                  }
               } else {
                  processErrorResponse(errors);
               }
            },
            error: function(jqXHR, errMsg) {
               // alert(errMsg);
               console.log(jqXHR);
               console.log(errMsg);
               alert("Please try again.");
            }
         });
         return false; // prevent default submit
      });
   }

   function processErrorResponse(errors){
      console.log("error!")
      var errorMsg = "";
      for (i = 0; i < Object.keys(errors).length; i++) {
         const attr = Object.keys(errors)[i];
         const msg = Object.values(errors)[i];
         console.log(attr);
         console.log(msg);
         var err = attr + ": " + msg;
         errorMsg += err;
         console.log(errorMsg);
      }
      alert(errorMsg)
   }

   $('#task-form-header').on('click', function(e) {
      e.preventDefault();
      $('#task-form-body').slideToggle();
   })

JS;
$this->registerJs($script);

?>

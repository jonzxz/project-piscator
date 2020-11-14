<?php

use yii\helpers\Html;
use yii\helpers\Url;
use yii\bootstrap4\ActiveForm;
use common\components\MyCustomActiveRecord;
use kartik\widgets\FileInput;
use kartik\select2\Select2;
use yii\web\JsExpression;

/**
 * @var yii\web\View $this
 * @var common\models\Bug $model
 */

$this->title = 'Create Bug';
$this->params['breadcrumbs'][] = ['label' => 'Bugs', 'url' => ['index']];
$this->params['breadcrumbs'][] = $this->title;
?>

<div class="bug-create">
  <div class="bug-form">
    <?php $form = ActiveForm::begin([ 'options' => ['enctype' => 'multipart/form-data'] ]); ?>
      <div class="card">

        <div class="card-body">
          <?= $form->errorSummary($model); ?>
          <?= $form->field($model, 'title')->textInput(['maxlength' => true]) ?>
          <?= $form->field($model, 'description')->textarea(['rows' => 6]) ?>

          <?= $form->field($model, 'documents[]')->widget(FileInput::classname(), [
              'options' => [
                  'multiple' => true
              ],
              'pluginOptions' => [
                  'allowedFileExtensions' => [
                      'jpg', 'jpeg', 'png', 'txt', 'csv', 'json', 'pdf'
                  ],
                  'uploadUrl' => Url::to('/bug/upload-file'),
                  'maxFileCount' => 5,
                  'showCancel' => false,
                  'showCaption' => false,
                  'showRemove' => false,
                  'showUpload' => false,
                  'dropZoneEnabled' => false,
              ],
              'pluginEvents' => [
                  'filebatchselected' => "function(event) {
                      $(this).fileinput('upload');
                  }",
                  'fileremoved' => "function(event, id, index) {
                       $.ajax({
                           type: 'POST',
                           url: '/bug/remove-file',
                           data: { filename: id.split('_').pop() }
                       });
                   }",
                  'fileclear' => "function(event) {
                      $.ajax({
                          type: 'POST',
                          url: '/bug/remove-file',
                          data: { delete_all: true }
                      });
                  }",
              ],
          ]) ?>

          <?= $form->field($model, 'tags')->widget(Select2::classname(),
              [
                  'theme' => Select2::THEME_MATERIAL,
                  'data' => $model->getCommonTags(),
                  'showToggleAll' => false,
                  'options' => [
                      'placeholder' => 'Select common tags or add your own ...',
                      'multiple' => true,
                  ],
                  'pluginOptions' => [
                      'tags' => true,
                      'tokenSeparators' => [ ',', ' ' ],
                      'maximumInputLength' => 15,
                      'allowClear' => true,
                      'createTag' => new JsExpression("function({ term, data }) {
                           return { id: term.toLowerCase(), text: term.toLowerCase() };
                       }")
                  ],
              ]
            ); ?>
        </div>

        <div class="card-footer">
          <?= Html::submitButton('Create', ['class' => 'btn btn-success'])?>
        </div>

      </div>
    <?php ActiveForm::end(); ?>
  </div>
</div>

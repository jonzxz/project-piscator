<?php

use yii\helpers\Url;
use yii\helpers\Html;
use yii\grid\GridView;
use common\models\Bug;
use common\models\User;

/**
 * @var yii\web\View $this
 * @var common\models\search\BugSearch $searchModel
 * @var yii\data\ActiveDataProvider $dataProvider
 */

$this->title = 'Bugs';
$this->params['breadcrumbs'][] = $this->title;
?>
<div class="bug-index">
    <div class="card">
        <?php
            if (Yii::$app->user->can(User::ROLE_DEVELOPER) || Yii::$app->user->can(User::ROLE_TRIAGER) || Yii::$app->user->can(User::ROLE_REVIEWER)){
                echo \backend\widgets\TabMenuBugWithTaskWidget::widget(['page'=>$page]);
            } else {
                echo \backend\widgets\TabMenuBugWidget::widget(['page'=>$page]);
            }
        ?>
        <div class="card-header">
            <?php echo Html::a('Create Bug', ['create'], ['class' => 'btn btn-success']) ?>
            <!-- <?php echo Html::a('All Bugs', ['index'], ['class' => 'btn btn-success']) ?> -->
            <!-- <?php echo Html::a('My Tasks', ['tasks'], ['class' => 'btn btn-success']) ?> -->
        </div>

        <div class="card-body p-0">
            <?php // echo $this->render('_search', ['model' => $searchModel]); ?>

            <?php echo GridView::widget([
                'layout' => "{items}\n{pager}",
                'options' => [
                    'class' => ['gridview', 'table-responsive'],
                ],
                'tableOptions' => [
                    'class' => ['table', 'text-nowrap', 'table-striped', 'table-bordered', 'mb-0'],
                ],
                'dataProvider' => $dataProvider,
                'filterModel' => $searchModel,
                'columns' => [
                    // ['class' => 'yii\grid\SerialColumn'],

                    'id',
                    [
                        'attribute'=>'title',
                        'format'=>'raw',
                        'value'=> function($model){
                            return Html::a($model->title, Url::to(['view','id'=>$model->id]));
                        }
                    ],
                    //'description:ntext',
                    'bug_status',
                    'priority_level',
                    [
                        'attribute'=>'created_at',
                        'format'=>'raw',
                        'value'=> function($model){
                            return Yii::$app->formatter->asDateTime($model->created_at);
                        }
                    ],
                    // 'developer_user_id',
                    // 'notes',
                    // 'delete_status',
                    // 'created_at',
                    // 'created_by',
                    // 'updated_at',
                    // 'updated_by',
                    [
                        'class' => \common\widgets\ActionColumn::class,
                        'template' => '{delete}',
                        'visibleButtons' => [
                            'delete' => function($model, $key, $index) {
                                return $model->created_by === Yii::$app->user->id &&
                                       $model->bug_status === Bug::BUG_STATUS_NEW;
                            }
                        ],
                    ],
                ],
            ]); ?>

        </div>
        <div class="card-footer">
            <?php echo getDataProviderSummary($dataProvider) ?>
        </div>
    </div>

</div>

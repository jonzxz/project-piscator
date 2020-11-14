<?php

use yii\helpers\Html;
use yii\helpers\Url;
use kartik\grid\GridView;
use common\models\SysAuditTrail;

/* @var $this yii\web\View */
/* @var $searchModel common\models\search\SysAuditTrailSearch */
/* @var $dataProvider yii\data\ActiveDataProvider */

$this->title = 'Audit Trail Logs';
$this->params['breadcrumbs'][] = $this->title;
?>
<div class="sys-audit-trail-index">

    <!-- <div class="audit-log">
    <?php

        $html = "<div class='log-list'>";
        $models =$dataProvider->models;

        echo \yii\widgets\LinkPager::widget([
            'pagination'=>$dataProvider->pagination,
        ]);

        foreach($models as $m) {
            $name = $m->created_by;
            $email = "";
            if ($m->user) {
                $name = $m->user->getPublicIdentity();
                $email = $m->user->email;
            }

            $by = "<b><i>" . utf8_decode($name) . "</i></b> &lt;".$email."&gt;";
            //$by = "dog";
            $d = Yii::$app->formatter->asDatetime($m->created_at);

            $link = '/activity-log/audit-trail-log-detail?id=' . $m->id;
            $html .= "<i class='text-muted small'>" . $d . "</i> - <span class='text-success'>[" . $m->controller . "/" . $m->action ."]</span> by " . $by . " <a href='" . $link . "'> <i class='fa fa-link'></i></a><br>";
        }
        $html .= "</div>";
        echo \yii\helpers\HtmlPurifier::process($html);

        echo \yii\widgets\LinkPager::widget([
            'pagination'=>$dataProvider->pagination,
        ]);
    ?>
    </div> -->

    <div class="card-body p-0">
        <?php
            echo GridView::widget([
                'layout' => "{items}\n{pager}",
                'options' => [
                    'class' => ['gridview', 'table-responsive'],
                ],
                'tableOptions' => [
                    ['table', 'text-nowrap', 'table-striped', 'table-bordered'],
                ],
                'dataProvider' => $dataProvider,
                'columns' => [

                    [
                        'attribute'=>'date',
                        'format'=>'raw',
                        'headerOptions' => ['width' => '15%'],
                        'value'=> function($model) {
                            return Yii::$app->formatter->asDateTime($model->created_at);
                        },
                        'contentOptions' => [
                            'class' => ['text-muted', 'font-italic']
                        ]
                    ],
                    [
                        'attribute'=>'action',
                        'format'=>'raw',
                        'headerOptions' => ['width' => '40%'],
                        'value'=>function($model) {
                            return Html::tag('span', '['.$model->controller."/".$model->action.']');
                        },
                        'contentOptions' => [
                            'class' => ['text-success']
                        ],
                    ],
                    [
                        'attribute'=>'User',
                        'format'=>'raw',
                        'headerOptions' => ['width' => '30%'],
                        'value'=>function($model) {
                            return Html::tag('span', $model->user->getPublicIdentity()." &lt;".$model->user->email."&gt;");
                        },
                        'contentOptions' => [
                            'class' => ['font-italic', 'font-weight-bold']
                        ],
                    ],
                    [
                        'attribute'=>'Link',
                        'format'=>'raw',
                        'headerOptions' => ['width' => '5%'],
                        'value'=> function($model) {
                            return Html::a('<i class="fa fa-link"></i>', '/activity-log/audit-trail-log-detail?id='.$model->id);
                        },
                    ],
                ],

            ])
        ?>


</div>

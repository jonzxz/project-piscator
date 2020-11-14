<?php

use yii\helpers\Html;
use yii\widgets\DetailView;

/* @var $this yii\web\View */
/* @var $model common\models\SysAuditTrail */


/* @var $this yii\web\View */
/* @var $model common\models\Trip */

$this->title = "Audit Trail Logs Detail";

$this->params['breadcrumbs'][] = ['label' => 'Sys Audit Trails', 'url' => ['audit-trail-log']];
$this->params['breadcrumbs'][] = $this->title;

$name = $model->created_by;
$email = "";
if ($model->user) {
    $name = $model->user->getPublicIdentity();
    $email = $model->user->email;
} 

$by = "<b><i>" . utf8_decode($name) . "</i></b> &lt;".$email."&gt;";
$d = Yii::$app->formatter->asDatetime($model->created_at);

$html = "";
$html .= "<i class='text-muted small'>" . $d . "</i><br>";
$html .= "<span class='text-success'>[" . $model->controller . "/" . $model->action ."]</span>";
$html .= " by  " . $by . "<br><br>";

$v = json_decode($model->value);

$html .= "<pre>";
$html .= print_r($v, true);
$html .= "</pre>";

echo \yii\helpers\HtmlPurifier::process($html);

?>
<?php

/**
 * @var yii\web\View $this
 * @var common\models\Bug $model
 */

$this->title = 'Update Bug: ' . ' ' . $model->title;
$this->params['breadcrumbs'][] = ['label' => 'Bugs', 'url' => ['index']];
$this->params['breadcrumbs'][] = ['label' => $model->title, 'url' => ['view', 'id' => $model->id]];
$this->params['breadcrumbs'][] = 'Update';
?>
<div class="bug-update">

    <?php echo $this->render('_form', [
        'model' => $model,
    ]) ?>

</div>

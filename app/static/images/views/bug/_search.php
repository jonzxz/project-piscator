<?php

use yii\helpers\Html;
use yii\bootstrap4\ActiveForm;

/**
 * @var yii\web\View $this
 * @var common\models\Bug $model
 * @var yii\bootstrap4\ActiveForm $form
 */
?>

<div class="bug-search">

    <?php $form = ActiveForm::begin([
        'action' => ['index'],
        'method' => 'get',
    ]); ?>

    <?php echo $form->field($model, 'id') ?>
    <?php echo $form->field($model, 'title') ?>
    <?php echo $form->field($model, 'description') ?>
    <?php echo $form->field($model, 'bug_status') ?>
    <?php echo $form->field($model, 'priority_level') ?>
    <?php // echo $form->field($model, 'developer_user_id') ?>
    <?php // echo $form->field($model, 'notes') ?>
    <?php // echo $form->field($model, 'delete_status') ?>
    <?php // echo $form->field($model, 'created_at') ?>
    <?php // echo $form->field($model, 'created_by') ?>
    <?php // echo $form->field($model, 'updated_at') ?>
    <?php // echo $form->field($model, 'updated_by') ?>

    <div class="form-group">
        <?php echo Html::submitButton('Search', ['class' => 'btn btn-primary']) ?>
        <?php echo Html::resetButton('Reset', ['class' => 'btn btn-secondary']) ?>
    </div>

    <?php ActiveForm::end(); ?>

</div>

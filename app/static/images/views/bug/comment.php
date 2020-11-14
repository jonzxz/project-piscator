<?php
use common\models\User;

?>

<div class="card">
    <div class="card-body">
        <?php echo $model->comment ?>
    </div>
    <div class="card-footer">
        <div class="d-flex flex-row-reverse">
            <i><?php echo Yii::$app->formatter->asDateTime($model->created_at)?></i>
            <div class="pr-3">
                <?php echo User::findIdentity($model->created_by)->publicIdentity?>
            </div>
        </div>
    </div>
</div>

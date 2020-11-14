<?php

use yii\helpers\Url;
use kartik\widgets\FileInput;

/**
* @var yii\web\View $this
* @var common\models\Bug $model
*/

$previews = $model->getDocumentPreviews();
$canEditAttachment = Yii::$app->user->id === $model->created_by;
?>

<div>
    <?= FileInput::widget([
        'name' => 'BugCreationForm[documents][]',
        'options' => [
         'multiple' => true
        ],
        'pluginOptions' => [
         'allowedFileExtensions' => [
             'jpg', 'jpeg', 'png', 'txt', 'csv', 'pdf', 'json'
         ],
         'uploadUrl' => Url::to('/bug/upload-file'),
         'uploadExtraData' => [
             'immediate' => true,
             'bug_id' => $model->id
         ],
         'maxFileCount' => 5,
         'showCancel' => false,
         'showCaption' => false,
         'showRemove' => false,
         'showUpload' => false,
         'showClose' => false,
         'showBrowse' => $canEditAttachment,
         'browseLabel' => 'Add Document',
         'dropZoneEnabled' => false,
         'initialPreview' => $previews['data'],
         'initialPreviewConfig'  => $previews['config'],
         'initialPreviewAsData' => true,
         'overwriteInitial' => false,
         'initialPreviewShowDelete' => $canEditAttachment,
         'deleteUrl' => Url::to('/bug/remove-file'),
         'initialPreviewDownloadUrl' => Url::to('/bug/download-file'),
         'msgUploadEmpty' => 'File already uploaded',
        ],
        'pluginEvents' => [
            'filebatchselected' => "function(event, files) {
                  $(this).fileinput('upload');
             }",
            'filepredelete' => "function(event) {
                return !confirm(`Are you sure you want to delete this file?`);
            }",
            // implemented to patch over buggy behaviour
            'filepreremove' => "function(event, id, index) {
                removeFile($model->id, event, id);
            }",
            'filesuccessremove' => "function(event, id) {
                removeFile($model->id, event, id);
            }",
        ],
    ]) ?>
</div>

<script type="text/javascript">
    function removeFile(bugId, event, fileId) {
        let thumbId = fileId.split('-').pop();
        if (hasUploadError(thumbId)) return;

        if (confirm(`Are you sure you want to delete this file?`)) {
            $.ajax({
                type: 'POST',
                url: '/bug/remove-file',
                data: {
                    filename: fileId.split('_').pop(),
                    immediate: true,
                    bug_id: bugId,
                }
            });
        } else {
            event.preventDefault();
        }
    }

    function hasUploadError(id) {
        return $(`[data-fileid='${id}']`).hasClass('file-preview-error');
    }
</script>

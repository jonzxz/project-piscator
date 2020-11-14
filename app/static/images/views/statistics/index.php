<?php

use yii\helpers\Html;
use yii\grid\GridView;
use kartik\export\ExportMenu;
use dosamigos\chartjs\ChartJs;
use common\models\Bug;
use common\models\User;
use rmrevin\yii\fontawesome\FAS;

use kartik\daterange\DateRangePicker;
use yii\data\ArrayDataProvider;
use kartik\form\ActiveForm;

$this->params['breadcrumbs'][] = 'Statistics';
?>
<style>
    .stat-arb {
        opacity: 0.8;
    }
    .stat-arb:hover {
        opacity: 1;
        text-shadow: 0 0 10px #000000;
    }
    .stacked-text {
        color: white;
    }

</style>

<div style="background-color: rgba(0,0,0,0.75); box-sizing: content-box !important;">
    <h1 class="pl-5" style="color: white;">Statistics</h1>
</div>
<div class="d-flex flex-column justify-content-between">
  <div class="d-flex flex-row">
    <div class="w-50">
      <?= ChartJs::widget([
        'type' => 'bar',
        'clientOptions' => [
          'height' => 100,
          'width' => 200,
          'title' => [
            'display' => true,
            'text' => 'No. of active bugs by Priority Level',
          ],
          'scales' => [
            'yAxes' => [[
              'ticks' => [
                'min' => 0,
              ],
              ]],
            ],
          ],
          'data' => [
            'labels' => ["Priority"],
            'datasets' => [
              [
                'label' => "Level 1",
                'backgroundColor' => "rgba(139,195,74,0.2)",
                'borderColor' => "rgba(139,195,74,1)",
                'pointBackgroundColor' => "rgba(179,181,198,1)",
                'pointBorderColor' => "#fff",
                'pointHoverBackgroundColor' => "#fff",
                'pointHoverBorderColor' => "rgba(179,181,198,1)",
                'data' => [$actBugPriority[0]['counter']],
              ],
              [
                'label' => "Level 2",
                'backgroundColor' => "rgba(255,235,59,0.2)",
                'borderColor' => "rgba(255,235,59,1)",
                'pointBackgroundColor' => "rgba(255,99,132,1)",
                'pointBorderColor' => "#fff",
                'pointHoverBackgroundColor' => "#fff",
                'pointHoverBorderColor' => "rgba(255,99,132,1)",
                'data' => [$actBugPriority[1]['counter']],
              ],
              [
                'label' => "Level 3",
                'backgroundColor' => "rgba(244,67,54,0.2)",
                'borderColor' => "rgba(244,67,54,1)",
                'pointBackgroundColor' => "rgba(255,99,132,1)",
                'pointBorderColor' => "#fff",
                'pointHoverBackgroundColor' => "#fff",
                'pointHoverBorderColor' => "rgba(255,99,132,1)",
                'data' => [$actBugPriority[2]['counter']],
              ],
            ],
          ],
        ]);
        ?>
      </div>
      <div class="w-50">
        <?php
            if(!array_search(date('m-Y'), array_column($reportedBugs, 'm_date'))){
                array_push($reportedBugs, array('m_date'=>date('m-Y'), 'counter'=>0));
            }
            if(!array_search(date('m-Y'), array_column($resolvedBugs, 'm_date'))){
                array_push($resolvedBugs, array('m_date'=>date('m-Y'), 'counter'=>0));
            }
        ?>
        <?= ChartJs::widget([
          'type' => 'line',
          'clientOptions' => [
            'height' => 100,
            'width' => 200,
            'title' => [
              'display' => true,
              'text' => 'Reported/resolved bugs',
            ],
          ],
          'data' => [
            'labels' => array_column($reportedBugs, 'm_date'),
            'datasets' => [
              [
                'label' => "Reported bugs",
                'backgroundColor' => "rgba(255,99,132,0.2)",
                'borderColor' => "rgba(255,99,132,1)",
                'pointBackgroundColor' => "rgba(255,99,132,1)",
                'pointBorderColor' => "#fff",
                'pointHoverBackgroundColor' => "#fff",
                'pointHoverBorderColor' => "rgba(255,99,132,1)",
                'data' => array_column($reportedBugs, 'counter')
              ],
              [
                'label' => "Resolved bugs",
                'backgroundColor' => "rgba(40,167,69,0.2)",
                'borderColor' => "rgba(40,167,69,1)",
                'pointBackgroundColor' => "rgba(40,167,69,1)",
                'pointBorderColor' => "#fff",
                'pointHoverBackgroundColor' => "#fff",
                'pointHoverBorderColor' => "rgba(40,167,69,1)",
                'data' => array_column($resolvedBugs, 'counter')
              ]
            ]
          ]
        ]);
        ?>
      </div>
      <div class="w-50 text-center">
        <?php if(sizeof($curBugStatus) === 0): ?>
            <b style="color:grey;font-size:14px;">Status of bugs this month</b><br>
            <p class="pt-5">No bugs created this month yet.</p>
        <? else: ?>
            <?= ChartJs::widget([
                'type' => 'pie',
                'clientOptions' => [
                    'height' => 100,
                    'width' => 200,
                    'title' => [
                        'display' => true,
                        'text' => 'Status of bugs this month',
                    ],
                    'elements' => [
                      'arc' => [
                        'borderWidth' => 1,
                      ],
                    ],
                ],
                'data' => [
                    'labels' => array_map('ucfirst', array_column($curBugStatus, 'bug_status')),
                    'datasets' => [
                        [
                            'backgroundColor' => [
                              "rgba(145,53,55,0.2)",
                              "rgba(121,119,108,0.2)",
                              "rgba(47,44,35,0.2)",
                              "rgba(229,210,225,0.2)",
                              "rgba(200,63,101,0.2)",
                              "rgba(183,130,112,0.2)",
                              "rgba(183,130,112,0.2)",
                              "rgba(204,187,192,0.2)",
                            ],
                            'pointBackgroundColor' => [
                              "rgba(145,53,55,1)",
                              "rgba(121,119,108,1)",
                              "rgba(47,44,35,1)",
                              "rgba(229,21125,1)",
                              "rgba(200,63,101,1)",
                              "rgba(183,130,112,1)",
                              "rgba(183,130,112,1)",
                              "rgba(204,187,192,1)",
                            ],
                            'pointBorderColor' => "#fff",
                            'pointHoverBackgroundColor' => "#fff",
                            'pointHoverBorderColor' => "rgba(179,181,198,1)",
                            'data' => array_column($curBugStatus, 'counter'),
                        ],
                    ]
                ]
            ]);
            ?>
        <?php endif; ?>
      </div>
    </div>
    <div class="d-flex flex-row justify-content-center">
      <div class="d-inline-flex flex-column w-25 m-3">
        <div class="card bg-danger text-white text-center stat-arb p-3">
          <b>Active bugs: <?php echo sizeof($actBugs) ?></b>
        </div>
        <div class="card bg-success text-white text-center stat-arb p-3">
          <b>Resolved bugs: <?php echo sizeof($resBugs) ?></b>
        </div>
        <div class="card bg-primary text-white text-center stat-arb p-3">
          <b>Bugs pending review: <?php echo sizeof($pendBugs) ?></b>
        </div>
      </div>
      <div class="card w-25 m-3">
        <div class="card-body">
          <div class="card-title">
            <b>Total Bugs</b>
          </div> <div class="card-text">
            <?php foreach($allBugStatus as $stat): ?>
              <?= ucfirst($stat['bug_status'])?>
              <span class="badge badge-secondary">
                <?= $stat['counter']?>
              </span><br>
            <?php endforeach; ?>
          </div>
        </div>
      </div>
      <div class="card d-flex flex-column w-25 m-3 p-3">
        <div class="card-title">
            <b>Bugs solved by our developers this month</b>
        </div>
        <div class="d-inline-flex flex-column justify-content-center mt-3">
          <?php
          $rank = [1,2,3];
          $colorArray = [
            "color: rgb(254,225,12)",
            "color: rgb(215,215,215)",
            "color: rgb(167,112,68)",
          ];
          foreach($devStats as $stats):
            ?>
              <div class="container mt-1">
                <?= FAS::stack()
                    ->on(FAS::icon('trophy',['style'=>array_shift($colorArray)]))
                    ->text(array_shift($rank), 
                        [
                            'class'=>'stacked-text'
                        ])
                ?>
                <b><?= User::findIdentity($stats['developer_user_id'])->username ?></b>
                <span class="badge badge-secondary">
                  <?= $stats['counter'] ?>
                </span>
              </div>
          <?php endforeach; ?>
        </div>
      </div>
    </div>
    <div class="d-inline-flex flex-row justify-content-center">
      <div class="card m-3">
        <div class="card-body">
          <div class="card-title">
            <b>Current bugs by Priority Level</b>
          </div>
          <div class="card-text pt-3">
            <?php foreach($actBugPriority as $level): ?>
              Priority Level <?= $level['priority_level']?>
              <span class="badge badge-secondary">
                <?= $level['counter']?>
              </span><br>
            <?php endforeach; ?>
          </div>
        </div>
      </div>
      <div class="card m-3">
        <div class="card-body">
          <div class="card-title">
            <b>Popular bug tags</b>
          </div>
          <div class="card-text pt-3">
            <?php foreach($bugTags as $tag): ?>
              <div>
              <?= $tag['name'] ?>
              <span class="badge badge-secondary">
                <?= $tag['counter'] ?>
              </span><br>
              </div>
            <?php endforeach; ?>
          </div>
        </div>
      </div>
      <div class="card m-3">
        <div class="card-body">
          <div class="card-title">
            <b>Bugs reported/resolved in <?php echo date('F')?></b>
          </div>
          <?php
          $curMonthRep = array();
          $curMonthRes = array();
          foreach($reportedBugs as $data){
            if($data['m_date'] === date('m-Y')){
              $curMonthRep = $data['counter'];
            }
          }
          
          foreach($resolvedBugs as $data){
            if($data['m_date'] === date('m-Y')){
              $curMonthRes = $data['counter'];
            }
          }

          ?>
          <div class="card-text d-flex flex-row justify-content-around pt-2">
            <div class="card bg-danger p-4 text-center">
                <b>Reported bugs</b>
                <?= FAS::icon('bug')->size(FAS::SIZE_2X)?>
                <b><?php echo $curMonthRep;?></b>
            </div>
            <div class="card bg-success p-4 text-center">
                <b>Resolved bugs</b>
                <?= FAS::icon('virus-slash')->size(FAS::SIZE_2X)?>
              <b><?php echo $curMonthRes;?></b>
            </div>
            </span><br>
          </div>
        </div>
      </div>
    </div>

    <hr class="w-100"/>
    <div style="background-color: rgba(0,0,0,0.75); box-sizing: content-box !important;">
        <h1 class="pl-5" style="color: white;">Statistics by date range</h1>
    </div>
    <div class="d-flex flex-row justify-content-center mt-5">
      <?php $form = ActiveForm::begin(['id' => 'export-form']) ?>
      <div class='col-md-12'>
        <?php
        echo $form->field($exportModel, 'date_range', [
          'addon'=>['prepend'=>['content'=>'<i class="fas fa-calendar-alt"></i>']],
          'options'=>['class'=>'drp-container form-group']
          ])->widget(DateRangePicker::classname(),[
            'value'=> $exportModel->date_range,
            'pluginOptions' => ['locale'=>['format'=>'YYYY-MM-DD']],
            'useWithAddon'=>true,
            'readonly' => true,
          ]);
          ?>
          <div class='card p-3'>
            <div class='d-flex flex-row'>
              <div class='btn-group-vertical mr-2'>
                <?php echo Html::submitButton('Get no. of Reported Bugs', ['name' => 'repb', 'class' => 'btn btn-light btn-md'])?>
                <?php echo Html::submitButton('Get no. of Resolved Bugs', ['name' => 'resb', 'class' => 'btn btn-light btn-md'])?>
                <?php echo Html::submitButton('Get top Reporters', ['name' => 'topr', 'class' => 'btn btn-light btn-md'])?>
                <?php echo Html::submitButton('Get top Developers', ['name' => 'topd', 'class' => 'btn btn-light btn-md'])?>
              </div>
              <div class='d-flex flex-column justify-content-center'>
                <?php
                // if top reporters/developers is pressed
                if($result instanceof ArrayDataProvider){
                  $header1 = $selection === 'topr' ? 'Bugs reported' : 'Bugs resolved';
                  $header2 = $selection === 'topr' ? 'Reported by' : 'Resolved by';
                  $attrb = $selection === 'topr' ? 'created_by' : 'developer_user_id';

                  echo Html::tag('h2', Html::encode(
                    $selection === 'topr' ? "Top reporters" : "Top developers"
                  ), ['class' => 'text-center']);

                  echo GridView::widget([
                    'dataProvider'=>$result,
                    'layout' => '{items}',
                    'columns' => [
                      [
                        'header' => $header1,
                        'attribute' => 'counter',
                      ],
                      [
                        'header' => $header2,
                        'attribute' => $attrb,
                        // using Closure to use outer variable
                        'value' => function($res) use ($attrb){
                          return User::findIdentity($res[$attrb])->username;
                        }
                      ],
                    ],
                  ]);
                } else {
                  if($selection != "")
                  echo Html::tag('h2', Html::encode(
                    $selection === 'repb' ? "Total no. of reported bugs"
                    : "Total no. of resolved bugs"
                  ), ['class' => 'text-center']);

                  echo Html::tag('h1', Html::encode($result),
                  ['class' => 'display-1 text-center pt-4']);
                }
                ?>
              </div>
            </div>
          </div>
        </div>
        <?php ActiveForm::end() ?>

      </div>

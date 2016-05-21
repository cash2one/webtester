/**
 * Created by Yajun Liu on 2016/5/21 0021.
 */
$(document).ready(function () {
        $('#taskTable').bootstrapTable(
            {
                url: '/show_post_list',
                queryParamsType: 'limit',
                striped: true,
                search: 'true',
                columns: [{
                    field: 'id',
                    title: 'ID',
                    sortable: true,
                    align: 'left',
                    width: '10%'
                }, {
                    field: 'name',
                    title: 'Name',
                    align: 'left',
                    width: '10%'
                }, {
                    field: 'ext',
                    title: 'Conf',
                    align: 'left',
                    width: '30%'
                }, {
                    field: 'exec_log',
                    title: 'Log',
                    align: 'left',
                    width: '30%'
                }, {
                    field: 'status',
                    title: 'Status',
                    align: 'left',
                    width: '10%'
                }
                    , {
                        field: 'id',
                        title: 'Operate',
                        align: 'center',
                        width: '10%',
                        // events: operateEvents,
                        formatter: operateFormatter
                    }
                ]
            }
        )
    }
);

function operateFormatter(value, row, index) {
    return '<a href="/show_post_report_html?post_id=' + value + '">show report</a>';
}
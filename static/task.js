/**
 * Created by Yajun Liu on 2016/5/21 0021.
 */
$(document).ready(function () {
        $('#taskTable').bootstrapTable(
            {
                url: '/show_post_list',
                queryParamsType: 'limit',
                columns: [{
                    field: 'id',
                    title: 'ID',
                    sortable: true,
                }, {
                    field: 'name',
                    title: 'Name'
                }, {
                    field: 'ext',
                    title: 'Conf'
                }, {
                    field: 'exec_log',
                    title: 'Log'
                }, {
                    field: 'id',
                    title: 'Operate',
                    align: 'center',
                    // events: operateEvents,
                    formatter: operateFormatter
                }
                ]
            }
        )
    }
);

function operateFormatter(value, row, index) {
    return '<a href="/show_post_report_html?post_id=' + value +'">show report</a>';
}
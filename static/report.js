$(document).ready(function () {
        $('#reportTable').bootstrapTable(
            {
                url: '/show_report_list',
                queryParamsType: 'limit',
                columns: [{
                    field: 'id',
                    title: 'ID'
                }, {
                    field: 'post_id',
                    title: 'Post'
                }, {
                    field: 'case_name',
                    title: 'Name'
                }, {
                    field: 'browser',
                    title: 'Browser'
                },{
                    field: 'resolution',
                    title: 'Resolution'
                },{
                    field: 'browser_size',
                    title: 'Browser Size'
                },{
                    field: 'result',
                    title: 'Result'
                },{
                    field: 'result_content',
                    title: 'Desc'
                }]
            }
        )
    }
);

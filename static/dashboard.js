var urlBtn = $('#urlBtn');
var addActionBtn = $('#addActionBtn');
var addCheckBtn = $('#addCheckBtn');
var addCaseBtn = $('#addCaseBtn');
var submitBtn = $('#submitBtn');

var urlInput = $('#urlInput');
var nameInput=$('#nameInput');
var cookieInput = $('#cookieInput');
var actionXpathInput = $('#actionXpathInput');
var actionDataInput = $('#actionDataInput');
var checkXpathInput = $('#checkXpathInput');
var checkDataInput = $('#checkDataInput');
var caseNameInput = $('#caseNameInput');
var windowScrollXInput = $('#windowScrollXInput');
var windowScrollYInput = $('#windowScrollYInput');

var actionTypeSelect = $('#actionTypeSelect');
var checkTypeSelect = $('#checkTypeSelect');
var screenResolutionSelect = $('#screenResolutionSelect');
var browserHighWidthSelect = $('#browserHighWidthSelect');
var browsersSelect = $('#browsersSelect');

var caseTable = document.getElementById('caseList').getElementsByTagName('tbody')[0];
var actionTable = document.getElementById('actionList').getElementsByTagName('tbody')[0];
var checkTable = document.getElementById('checkList').getElementsByTagName('tbody')[0];

var iframePage = $('#iframePage');

var xpathInput = actionXpathInput;

var caseList = [];
var currentCase = {};
var actionList = [];
var checkList = [];
var currentAction = {};
var currentCheck = {};

var url = undefined;
var oldElemList = [];
var cookie_list=undefined;

urlBtn.click(function () {
    url=urlInput.val();
    cookie_list=cookieInput.val();
    $('#formUrl').val(url);
    $('#formCookie').val(cookie_list);
    $('#hiddenForm').submit();
});

actionXpathInput.click(
    function () {
        xpathInput = actionXpathInput;
    }
);


function makeEleRedBorder(value) {
    if (value != '') {
        for (var i = 0; i < oldElemList.length; i++) {
            $(oldElemList[i]).css("border", "");
        }
        var elemList = iframePage.contents().xpathEvaluate(value);
        oldElemList = elemList;
        for (var i = 0; i < elemList.length; i++) {
            var elem = elemList[i];
            $(elem).css("border", "3px solid red")
        }
    }
};

checkXpathInput.click(
    function () {
        xpathInput = checkXpathInput;
    }
);

addCaseBtn.click(function () {
    var name = caseNameInput.val();
    url = urlInput.val();
    currentCase.url = url;
    currentCase.name = name;
    currentCase.browserWindowSize = [];
    var inputWindowSizeList = browserHighWidthSelect.val();
    for (var i = 0; i < inputWindowSizeList.length; i++) {
        currentCase.browserWindowSize.push(formatResolution(inputWindowSizeList[i]));
    }
    currentCase.screenResolution = formatResolution(screenResolutionSelect.val());
    currentCase.browserScrollPosition = {x: parseInt(windowScrollXInput.val()), y: parseInt(windowScrollYInput.val())};
    currentCase.browsers = browsersSelect.val();
    currentCase.actionList = actionList;
    currentCase.checkList = checkList;
    caseList.push(currentCase);
    var newRow = caseTable.insertRow(caseTable.rows.length);
    var nameCell = newRow.insertCell(0);
    aNode = $('<a>');
    aNode.text(currentCase.name);
    $(nameCell).append(aNode);
    $(aNode).editable(
        {
            type: 'text',
            title: 'Enter Case Name',
            success: function (response, newValue) {
                var index = $(this).parent().closest('tr').index();
                var myCase = caseList[index];
                myCase.name = newValue;
                caseList[index] = myCase;
            }
        }
    );

    var urlCell = newRow.insertCell(1);
    var aNode = $('<a>');
    aNode.text(currentCase.url);
    $(urlCell).append(aNode);
    $(aNode).editable(
        {
            type: 'text',
            title: 'Enter Case Url',
            success: function (response, newValue) {
                var index = $(this).parent().closest('tr').index();
                var myCase = caseList[index];
                myCase.url = newValue;
                caseList[index] = myCase;
            }
        }
    );

    var deleteBtnCell = newRow.insertCell(2);
    var deleteBtn = $('<button>');
    deleteBtn.text('delete').attr('class', 'btn btn-danger btn-sm');
    deleteBtn.click(
        function () {
            var index = $(this).parent().closest('tr').index();
            caseList.splice(index, 1);
            caseTable.deleteRow(index);
        }
    );
    $(deleteBtnCell).append(deleteBtn);

    console.log(JSON.stringify(caseList));
    actionList = [];
    checkList = [];
    currentCase = {};
});

addActionBtn.click(
    function () {
        currentAction.xpath = actionXpathInput.val();
        currentAction.actionType = actionTypeSelect.val();
        currentAction.input = actionDataInput.val();
        actionList.push(currentAction);

        var newRow = actionTable.insertRow(caseTable.rows.length);
        var xpathCell = newRow.insertCell(0);
        aNode = $('<a>');
        aNode.text(currentAction.xpath);
        $(xpathCell).append(aNode);
        $(aNode).editable(
            {
                type: 'text',
                title: 'Enter Xpath',
                success: function (response, newValue) {
                    var index = $(this).parent().closest('tr').index();
                    var myCase = actionList[index];
                    myCase.xpath = newValue;
                    actionList[index] = myCase;
                }
            }
        );

        var typeCell = newRow.insertCell(1);
        aNode = $('<a>');
        aNode.text(currentAction.actionType);
        $(typeCell).append(aNode);
        $(aNode).editable(
            {
                type: 'select',
                title: 'Select Type',
                source: [
                    {
                        value: 'clear',
                        text: 'clear'
                    },
                    {
                        value: 'click',
                        text: 'click'
                    },
                    {
                        value: 'sentkey',
                        text: 'sentkey'
                    }
                ],
                success: function (response, newValue) {
                    var index = $(this).parent().closest('tr').index();
                    var myCase = actionList[index];
                    myCase.actionType = newValue;
                    actionList[index] = myCase;
                }
            }
        );

        var inputCell = newRow.insertCell(2);
        var aNode = $('<a>');
        aNode.text(currentAction.input);
        $(inputCell).append(aNode);
        $(aNode).editable(
            {
                type: 'text',
                title: 'Enter Input',
                success: function (response, newValue) {
                    var index = $(this).parent().closest('tr').index();
                    var myCase = actionList[index];
                    myCase.input = newValue;
                    actionList[index] = myCase;
                }
            }
        );

        var deleteBtnCell = newRow.insertCell(3);
        var deleteBtn = $('<button>');
        deleteBtn.text('delete').attr('class', 'btn btn-danger btn-sm');
        deleteBtn.click(
            function () {
                var index = $(this).parent().closest('tr').index();
                actionList.splice(index, 1);
                actionTable.deleteRow(index);
            }
        );
        $(deleteBtnCell).append(deleteBtn);

        currentAction = {};
        console.log(JSON.stringify(actionList));
    }
);

addCheckBtn.click(
    function () {
        currentCheck.xpath = checkXpathInput.val();
        currentCheck.checkType = checkTypeSelect.val();
        currentCheck.checkData = checkDataInput.val();
        checkList.push(currentCheck);

        var newRow = checkTable.insertRow(caseTable.rows.length);
        var xpathCell = newRow.insertCell(0);
        aNode = $('<a>');
        aNode.text(currentCheck.xpath);
        $(xpathCell).append(aNode);
        $(aNode).editable(
            {
                type: 'text',
                title: 'Enter Xpath',
                success: function (response, newValue) {
                    var index = $(this).parent().closest('tr').index();
                    var myCase = actionList[index];
                    myCase.xpath = newValue;
                    checkList[index] = myCase;
                }
            }
        );

        var typeCell = newRow.insertCell(1);
        aNode = $('<a>');
        aNode.text(currentCheck.checkType);
        $(typeCell).append(aNode);
        $(aNode).editable(
            {
                type: 'select',
                title: 'Select Type',
                source: [

                    {
                        value: 'expectedText',
                        text: 'expectedText'
                    },
                    {
                        value: 'expectedUrl',
                        text: 'expectedUrl'
                    },
                    {
                        value: 'printScreen',
                        text: 'printScreen'
                    }
                ],
                success: function (response, newValue) {
                    var index = $(this).parent().closest('tr').index();
                    var myCase = checkList[index];
                    myCase.checkType = newValue;
                    checkList[index] = myCase;
                }
            }
        );

        var inputCell = newRow.insertCell(2);
        var aNode = $('<a>');
        aNode.text(currentCheck.checkData);
        $(inputCell).append(aNode);
        $(aNode).editable(
            {
                type: 'text',
                title: 'Enter Input',
                success: function (response, newValue) {
                    var index = $(this).parent().closest('tr').index();
                    var myCase = actionList[index];
                    myCase.checkData = newValue;
                    checkList[index] = myCase;
                }
            }
        );

        var deleteBtnCell = newRow.insertCell(3);
        var deleteBtn = $('<button>');
        deleteBtn.text('delete').attr('class', 'btn btn-danger btn-sm');
        deleteBtn.click(
            function () {
                var index = $(this).parent().closest('tr').index();
                checkList.splice(index, 1);
                checkTable.deleteRow(index);
            }
        );
        $(deleteBtnCell).append(deleteBtn);
        currentCheck = {};
        console.log(JSON.stringify(checkList));
    }
);

submitBtn.click(
    function () {
        console.log(JSON.stringify({name:nameInput.val(),caseList: caseList}));
        $.post('/add_post',
            {test_post: JSON.stringify({caseList: caseList})},
            function (data) {
                //noinspection JSUnresolvedVariable
                if (data.errno == 0) {
                    $('#submitMsg').html(makeAlertDom(data.msg, "alert alert-success"));
                } else {
                    $('#submitMsg').html(makeAlertDom(data.msg, "alert alert-danger"));
                }
            }
        ).error(
            function () {
                $('#submitMsg').html(makeAlertDom("post error", "alert alert-danger"));
            }
        );
    }
);

iframePage.load(
    function () {
        var contents = iframePage.contents();
        var elements = contents[0].all;
        for (var i = 0; i < elements.length; i++) {
            elements[i].onclick = function (event) {
                event.preventDefault();// 取消事件的默认行为
                event.stopPropagation(); // 阻止事件的传播
                var xpathString = createXPathFromElement(elements,this);
                xpathInput.val(xpathString).focus();
                makeEleRedBorder(xpathString);
            }
        }
    }
);

function makeAlertDom(text, msgClass) {
    var msg = $('<div>');
    msg.attr('class', msgClass);
    msg.attr('role', 'alert');
    msg.text(text);
    return msg;
}

function createXPathFromElement(allNodes,elm) {
    for (var segs = []; elm && elm.nodeType == 1; elm = elm.parentNode) {
        if (elm.hasAttribute('id')) {
            var uniqueIdCount = 0;
            for (var n = 0; n < allNodes.length; n++) {
                if (allNodes[n].hasAttribute('id') && allNodes[n].id == elm.id) uniqueIdCount++;
                if (uniqueIdCount > 1) break;
            }
            if (uniqueIdCount == 1) {
                segs.unshift('id("' + elm.getAttribute('id') + '")');
                return segs.join('/');
            } else {
                segs.unshift(elm.localName.toLowerCase() + '[@id="' + elm.getAttribute('id') + '"]');
            }
        } else if (elm.hasAttribute('class')) {
            segs.unshift(elm.localName.toLowerCase() + '[@class="' + elm.getAttribute('class') + '"]');
        } else {
            for (var i = 1, sib = elm.previousSibling; sib; sib = sib.previousSibling) {
                if (sib.localName == elm.localName)  i++;
            }
            segs.unshift(elm.localName.toLowerCase() + '[' + i + ']');
        }
    }
    return segs.length ? '/' + segs.join('/') : null;
};

function formatResolution(resolution) {
    var widthHigh = resolution.split('x');
    return {width: parseInt(widthHigh[0]), high: parseInt(widthHigh[1])};
}

$.fn.xpathEvaluate = function (xpathExpression) {
    // NOTE: vars not declared local for debug purposes
    var $this = this.first(); // Don't make me deal with multiples before coffee

    // Evaluate xpath and retrieve matching nodes
    var xpathResult = this[0].evaluate(xpathExpression, this[0], null, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);

    var result = [];
    var elem = undefined;
    while (elem = xpathResult.iterateNext()) {
        result.push(elem);
    }

    $result = jQuery([]).pushStack(result);
    return $result;
}
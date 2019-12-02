$(document).ready(function() {

    $('.topic-btn').click(function () {
        alert("hola!");
    });

    $('.topic-btn-selected').click(function () {
        $(this).removeClass('topic-btn-selected');
    });
});
setTimeout(function () {$('#notification').addClass('hidden')}, 1500);

function textAreaAdjust(o) {
    o.style.height = "1px";
    o.style.height = (25 + o.scrollHeight) + "px";
}
$('input[type=radio][name=category_choice]').change(function() {
    if (this.value === 'existing') {
        $('#category_id').html(
            '<select name="category_name"> {% for item in all_categories  %} <option value="{{item.category_name }} ">' +
            ' {{item.category_name }}</option>\n' +
            '{% endfor %} </select>'
        );
    }
    else if (this.value === 'new') {
        $('#category_id').html('<input type="text" name="category_name">');
    }
});

$(document).ready(function () {

    $('input[type=radio][name=category_choice]').change(function() {
    if (this.value === 'existing') {

        alert("EXISTING");
    }
    else if (this.value === 'new') {
       alert("NEW");
    }
});




});

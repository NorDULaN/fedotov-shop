$(document).ready(function(){
  var form = $('#form_buying_product');
  console.log(form);
  form.on('submit', function(e){
    e.preventDefault();
    var item_quantity = $('#fbp_item_quantity').val();
    console.log(item_quantity);
    var submit = $('#fbp_submit');
    var item_id = submit.data("item_id");
    console.log(item_id);
    var item_name = submit.data("item_name");
    console.log(item_name);
    var item_price = submit.data("item_price");
    console.log(item_price);

    var data = {};
    data.item_id = item_id;
    data.item_quantity = item_quantity;
    var csrf_token = getCookie('csrftoken');
    data["csrfmiddlewaretoken"] = csrf_token;
    var url = form.attr("action");

    $.ajax({
      url:url,
      type: 'POST',
      data: data,
      cache: true,
      success: function(data){
        console.log("OK");
      },
      error: function(){
        console.log("ERROR")
      }
    })

  })
});

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

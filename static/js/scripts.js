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
  })
});

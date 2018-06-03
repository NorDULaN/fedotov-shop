$(document).ready(function(){
   var form = $('#form_buying_product');

   // Функция обновления корзины
   function cartUpdate(item_id, item_quantity)
   {
      var data = {};
      data.item_id = item_id;
      data.item_quantity = item_quantity;
      var csrf_token = getCookie('csrftoken');
      data["csrfmiddlewaretoken"] = csrf_token;
      var url = form.attr("action");
      $.ajax({
         url: url,
         type: 'POST',
         data: data,
         cache: true,
         success: function(data)
         {
            console.log("OK");
            if(data.items_in_cart_count)
            {
               $('#items_in_cart_count').text(" " + data.items_in_cart_count + " ")
            }
            if(data.items_in_cart_price)
            {
               $('#items_in_cart_price').text(data.items_in_cart_price + " руб.")
            }
         },
         error: function()
         {
            console.log("ERROR")
         }
      })
   }

   // Страница с товаром - Кнопка Добавить в корзину
   form.on('submit', function(e)
   {
      e.preventDefault();
      var item_quantity = $('#fbp_item_quantity').val();
      var submit = $('#fbp_submit');
      var item_id = submit.data("item_id");
      var item_name = submit.data("item_name");
      var item_price = submit.data("item_price");
      cartUpdate(item_id, item_quantity)
   });

   // Пересчёт деталей заказа
      function calcCheckOut()
      {
         var total_price = 0;
         $('.item-total-price').each(function(){
            total_price = total_price + parseFloat($(this).text().replace(',','.'));
         });

         $('#end_price').text(total_price.toFixed(2) + " руб.");
   };

   // Изменения кол-во товара на странице чекаута
   $(document).on('change', ".items-in-stack", function(){
      var current_count = $(this).val();
      if(current_count < 1) current_count=1;
      var current_div = $(this).closest('div');
      var current_index = parseInt(current_div.find('.item-index').text());
      var current_id = parseInt(current_div.find('.item-id').text());
      var current_price = parseFloat(current_div.find('.item-price').text().replace(',','.'));
      var current_price_d = parseFloat(current_div.find('.item-price-d').text().replace(',','.'));
      if(current_price_d>0)
         $('#item_total_price' + current_index).text(parseFloat(current_count*current_price_d).toFixed(2));
      else
         $('#item_total_price' + current_index).text(parseFloat(current_count*current_price).toFixed(2));
      $('#item_count' + current_index).text(current_count);
      var data = {};
      var csrf_token = getCookie('csrftoken');
      data["csrfmiddlewaretoken"] = csrf_token;
      var order = {
         id: current_id,
         count: current_count
      };
      $.extend(true, data, order);
      $.ajax({
         url: 'continue',
         type: 'POST',
         data: data,
         cache: true,
         success: function(data)
         {
            console.log("OK");
            if(data.items_in_cart_count)
            {
               $('#items_in_cart_count').text(" " + data.items_in_cart_count + " ")
            }
            if(data.items_in_cart_price)
            {
               $('#items_in_cart_price').text(data.items_in_cart_price + " руб.")
            }
         },
         error: function()
         {
            console.log("ERROR")
         }
      })
      calcCheckOut(); // Авто-пересчёт деталей заказа
   });
   calcCheckOut(); // Авто-пересчёт деталей заказа
   // Удаление из корзины
   $(document).on('click', ".close2", function(){
      var current_div = $(this).closest('div');
      var current_index = parseInt(current_div.find('.item-index').text());
      var current_id = parseInt(current_div.find('.item-id').text());
      $('#x_span' + current_index).empty();
      $('#x_div' + current_index).empty();

      var data = {};
      var csrf_token = getCookie('csrftoken');
      data["csrfmiddlewaretoken"] = csrf_token;
      data["is_delete"] = true;
      var order = {
         id: current_id,
         count: 0
      };
      $.extend(true, data, order);
      $.ajax({
         url: 'remove',
         type: 'POST',
         data: data,
         cache: true,
         success: function(data)
         {
            console.log("OK");
            if(data.items_in_cart_count || data.items_in_cart_count == 0)
            {
               //console.log(data.items_in_cart_count);
               $('#items_in_cart_count').text(" " + data.items_in_cart_count + " ")
               $('#tt_count').text(data.items_in_cart_count)
            }
            if(data.items_in_cart_price || data.items_in_cart_price == 0)
            {
               //console.log(data.items_in_cart_price);
               $('#items_in_cart_price').text(data.items_in_cart_price + " руб.")
            }
         },
         error: function()
         {
            console.log("ERROR")
         }
      })
      calcCheckOut(); // Авто-пересчёт деталей заказа
   });



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

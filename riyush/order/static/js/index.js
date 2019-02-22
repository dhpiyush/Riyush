
function slot_button_click(){
	var $button = $(this);
	$('.slot_button').removeClass('grey');
	$button.addClass('grey');
    console.log(this.id);
}

$("#people_count").submit( function(event) {
	var count = $('.people').val();
	var rest_id = $('.people').attr('id');
    console.log(rest_id);

    $('.time_slots').text('');
    $('.loader_container').show();

    $.post("/available_slots",{'rest_id': rest_id, 'people_count': count},function(data){
    	console.log('available_slots success');
    	console.log(JSON.parse(data.slots).length);

    	var slots = JSON.parse(data.slots);
    	for(var i=0; i< slots.length;i++){
    		// var btn = '<button class="btn slot_button" style="margin-right: 5px" id='+ slots[i].rest_timings_id +'>'+ slots[i].slot +'</button>'
    		var btn = document.createElement('button');
    		btn.className = "btn slot_button";
    		btn.innerHTML = slots[i].slot;
    		btn.id = slots[i].rest_timings_id;
    		btn.onclick = slot_button_click;
    		$('.time_slots').append(btn);
    	}

    })
      .fail(function() {
	    console.log('available_slots Error');
	  })
	  .always(function() {
	    console.log( "finished" );
	    $('.loader_container').hide();
	  });
    event.preventDefault();
});
$(".slot_button").on('click', function(event) {
	var $button = $(this);
	$('.slot_button').removeClass('grey');
	$button.addClass('grey');
    console.log(this.id);
});

$(".order_completed_confirm").on('click', function(event) {
	var $button = $(this);
	var id = $button.attr('id');
	var rest_timings_id = $('.slot_id').attr('id');
	var modal_id = '#data-target-' + $button.attr('id');
	var order_id = '#order' + $button.attr('id');
	$(modal_id).closeModal();
	$(order_id).remove();
	$.post("/order_complete",{'order_id': id,'rest_timings_id':rest_timings_id},function(data){
		Materialize.toast('Order Completed ', 2000)
    	console.log(data);
    })
      .fail(function() {
	    console.log('Error');
	  });
	console.log(id);
	
});

$("#order_button").on('click', function(event) {
	var time = $('.time_slots').find('.grey').attr('id');
	// time is id of the row of restauranttimings table
	if(time){
		window.location = "/menu/" + time;
	}
	else{
		Materialize.toast('Please select time slot ', 2000);
	}
	
});
var basket_data = {};

// $(".change_value").on("click", function() {
//   var $button = $(this);
//   var oldValue = $button.parent().find("input").val();
//   var id = $button.parent().find("input").attr('id');

//   console.log(id);

//   if ($button.text() == "+") {
//     var newVal = parseInt(oldValue) + 1;
//   } else {
//    // Don't allow decrementing below zero
//     if (oldValue >= 1) {
//       var newVal = parseInt(oldValue) - 1;
//     } else {
//       newVal = 0;
//     }
//   }

//   $button.parent().find("input").val(newVal);
//   basket_data[id] = newVal;

//   var count = 0;
//   $.each(basket_data, function(key,value){
//   	count = count + value;
//   });

//   $('.basket').text(count);
//   console.log(basket_data);

// });

function update_basket(item,price,val,id){
  var product_details = {};
  product_details['name'] = item;
  product_details['price'] = price;
  product_details['quantity'] = val;
  product_details['id'] = id;
  basket_data[id] = product_details;
}

var total_price = 0;

function update_order(){
	$('.order').text('');
	total_price = 0;
    $.each(basket_data, function(key,value){
	  	if (value['quantity']!=0) {
	  		var item_details = '<div class="col s12 item">'+
									'<div>'+
										'<div class="col s9">'+
											value['name']+
										'</div>'+
										'<div class="col s3">'+
											value['quantity']*value['price']+
										'</div>'+
									'</div>'+
									'<div class="col s12">'+
										value['quantity']+ ' x '+ value['price'] + 
									'</div>'+					
								'</div>';
			$('.order').append(item_details);
			total_price = total_price + value['price']*value['quantity'];
	  	}
    });
    $('.total-price-val').text(total_price);
}

$(".inc_value").on("click", function() {
  var $button = $(this);
  var oldValue = $button.parent().find("input").val();
  var id = parseInt($button.parent().find("input").attr('id'));
  var item = $button.parent().find("input").attr('name');
  var price = parseInt($button.parent().find("input").attr('price'));
  // console.log(item);

  var newVal = parseInt(oldValue) + 1;
  $button.parent().find("input").val(newVal);

  // var product_details = {};
  // product_details['name'] = item;
  // product_details['price'] = price;
  // product_details['quantity'] = newVal;
  // product_details['id'] = id;
  // basket_data[id] = product_details;
  update_basket(item,price,newVal,id);
  update_order();

  // oldBasketCount = parseInt($('.basket').text());

  // var count = 0;
  // $.each(basket_data, function(key,value){
  // 	count = count + value['quantity'];
  // });

  // $('.basket').text(count);
  console.log(basket_data);

  Materialize.toast('Added Item ', 1000)

});

$(".dec_value").on("click", function() {
  var $button = $(this);
  var oldValue = $button.parent().find("input").val();
  var id = parseInt($button.parent().find("input").attr('id'));
  var item = $button.parent().find("input").attr('name');
  var price = parseInt($button.parent().find("input").attr('price'));

  // console.log(id);

  oldBasketCount = parseInt($('.basket').text());
  if (oldValue >= 1) {
    var newVal = parseInt(oldValue) - 1;
    Materialize.toast('Removed Item ', 1000)
    
  } else {
    newVal = 0;
  }
  $button.parent().find("input").val(newVal);
  update_basket(item,price,newVal,id)
  update_order()
  // basket_data[id] = newVal;

  // var count = 0;
  // $.each(basket_data, function(key,value){
  // 	count = count + value['quantity'];
  // });

  // $('.basket').text(count);
  console.log(basket_data);
});

$(".checkout").on("click", function(){
	var price = $('.total-price-val').text().trim();
	var rest_timings_id = $('.checkout').attr('id').split('_')[2];

	console.log('basket',rest_timings_id);
	if (price == '0') {
		Materialize.toast("Please Order Food", 4000);
	}
	else{
		var payment_result;
		var order_details;
		data1 = {'price':total_price*100,'basket_data':JSON.stringify(basket_data),'rest_timings_id':rest_timings_id}
		$.post( "/payment", data1 ,function(data) {
			order_details = data.order_details;	
			console.log( order_details);
			var options = {
			  "key": "rzp_test_aF4TBXHQqj0x7T",
			  "amount": total_price*100, // 2000 paise = INR 20
			  "name": "Riyush",
			  "description": "Pre-Book Table and Order Food",
			  // "image": "/your_logo.png",
			  "order_id": order_details['id'],
			  "handler": function (response){
			  	payment_details = response;
			  	// payment_details = {razorpay_payment_id: "pay_Bu68AUjGPpqhJf", razorpay_order_id: "order_Bu6846KOCYxSNi", razorpay_signature: "bbe38bf2df531d19708c64d76537f1a032f908d55bbfed8bb9b1bda5fe603a71"}
			    payment_details['amount'] = total_price*100;
			    payment_details['rest_timings_id'] = rest_timings_id
			    console.log(payment_details);
			    $.post("/payment_details",payment_details,function(data){

			    	console.log('payment_details store success');
			    	window.location = "/payment/success";
			    })
			      .fail(function() {
				    console.log('payment_details store Error');
				  })
				  .always(function() {
				    console.log( "finished" );
				  });
			  },
			  "prefill": {
			      // "name": "Gaurav Kumar",
			      // "email": "test@test.com"
			  },
			  "notes": {
			      "Book Table": "Order Food"
			  },
			  "theme": {
			      "color": "#F44336 "
			  }
			};
			var rzp1 = new Razorpay(options);
			console.log(basket_data);
			rzp1.open();
		})
		  .fail(function() {
		    Materialize.toast("Error Occured", 4000);
		  })
		  .always(function() {
		    console.log( "finished" );
		  });
	}

});




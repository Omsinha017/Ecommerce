$(document).ready(function(){
  // contact form handler 
  var contactForm = $(".contact-form")
  var contactFormMethod = contactForm.attr("method")
  var contactFormEndpoint = contactForm.attr("action")
  
  function displaySubmit(submitBtn, defaultText, dosubmit){
    if (dosubmit){
      submitBtn.addClass("disabled")
      submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Sending...")
    }else{
      submitBtn.removeClass("disabled")
      submitBtn.html(defaultText)
    }
  }


  contactForm.submit(function(event){
    event.preventDefault()
    var contactFormSubmitBtn = contactForm.find("[type='submit']")
    var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()
    var contactFormData = contactForm.serialize()
    var thisForm = $(this)

    displaySubmit(contactFormSubmitBtn, "", true)
    $.ajax({
      method : contactFormMethod,
      url : contactFormEndpoint,
      data : contactFormData,
      success : function(data){
        contactForm[0].reset()
        $.alert({
            title: 'Success',
            content: data.message,
            theme: 'modern',
          })
          setTimeout(function(){
            displaySubmit(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
          },1000)
      },
      error : function(error){
        var jsonData = error.responseJSON
        var msg = ""

        $.each(jsonData, function(key,value){
          msg += key + ": " + value[0].message + "<br>"
        })
        $.alert({
            title: 'Oops!',
            content: msg,
            theme: 'modern',
          })
          setTimeout(function(){
            displaySubmit(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
          },1000)
      }
    })
  })


  // Auto Search
  var searchform = $(".search-form")
  var searchInput = searchform.find("[name='q']")   // input name = 'q'
  var typingTimer;
  var typingInterval = 1500   // 1.5 seconds
  var searchBtn = searchform.find("[type='submit']")

  searchInput.keyup(function(event){
    // key released
    clearTimeout(typingTimer)
    typingTimer = setTimeout(performSearch,typingInterval) 
  })

  searchInput.keydown(function(event){
    // key pressed
    clearTimeout(typingTimer)
  })

  function performSearch(){
    searchBtn.addClass("disabled")
    searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...")
    var query = searchInput.val()
    window.location.href = '/search/?q=' + query
    
  }


  // cart + add products

  var productForm = $(".form-product-ajax")
  function getOwnedProduct(productId,submitSpan){
    var actionEndPoint = '/orders/endpoint/verify/ownership/'
    var httpMethod = 'GET'
    var data = {
      product_id : productId
    }
    var isOwner;
    $.ajax({
      url : actionEndPoint,
      method : httpMethod,
      data : data,
      success : function(data){
        if (data.owner){
          isOwner = true
          submitSpan.html('<a class="btn btn-link" href="/library/"> In Library </a>')
        }else{
          isOwner = false
        }
      },
      error : function(err){
          console.log(err);
      }
  })
  return isOwner
}


$.each(productForm,function(){
    var $this = $(this)
    var isUser = $this.attr("data-user")
    var submitSpan = $this.find(".submit-span")
    var productInput = $this.find("[name='product_id']")
    var productId = productInput.attr("value")
    var productIsDigital = productInput.attr("data-is-digital")
    var isOwned;
    if (productIsDigital && isUser){
      isOwned = getOwnedProduct(productId,submitSpan)
  }
})


  productForm.submit(function(e){
    e.preventDefault();
    var thisForm = $(this)
    var actionEndPoint = thisForm.attr("data-endpoint")
    var httpMethod = thisForm.attr("method")
    var formData = thisForm.serialize()

    $.ajax({
        url : actionEndPoint,
        method : httpMethod,
        data : formData,
        success : function(data){
          console.log("yes it's working")
          getOwnedProduct()
          var submitSpan = thisForm.find(".submit-span");
          if (data.added){
            submitSpan.html('<div class="btn-group"><a class="btn btn-link" href="/cart/"> In Cart </a> <button type="submit" class="btn btn-link">Remove?</button></div>');
          }else{
            submitSpan.html('<button type="submit" class="btn btn-success"> Add to Cart </button>');
          }
          var navbarCount = $(".navbar-cart-count")
           navbarCount.text(data.CartItemCount)

          if(window.location.href.indexOf("cart")!= -1){
            refreshCart()
          }
        },
        error : function(edata){
          $.alert({
            title: 'Oops!',
            content: 'An Error Occured!',
            theme: 'modern',
          })
        }
    })
  })

  function refreshCart(){
    var cartTable = $(".cart-table")
    var cartBody = cartTable.find(".cart-body")
    
    var productRows = cartBody.find(".cart-product")
    var currentUrl = window.location.href

    var refreshCartUrl = '/api/cart/'
    var refreshCartMethod = "GET"
    var data = {}
    $.ajax({
      url : refreshCartUrl,
      method : refreshCartMethod,
      data : data,
      success : function(data){
        var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
        if(data.products.length > 0 ){
          productRows.html("")
          i = data.products.length
          $.each(data.products,function(index,value){
            var newCartItemRemove = hiddenCartItemRemoveForm.clone()
            newCartItemRemove.css("display","block")
            newCartItemRemove.find(".cart-item-product-id").val(value.id)
            cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href='" + value.url + "'>" + value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
            i--
          })
          cartBody.find(".cart-subtotal").text(data.subtotal)
          cartBody.find(".cart-total").text(data.total)
        }else
          window.location.href = currentUrl
      },
      error : function(e){
        $.alert({
            title: 'Oops!',
            content: 'An Error Occured!',
            theme: 'modern',
          })
      }
    })
  }
})

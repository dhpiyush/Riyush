(function ($) {
  $(function () {
    $('select').material_select()

    $('.button-collapse').sideNav();
    $('.parallax').parallax();

    $(document).ready(function () {
      $('.materialboxed').materialbox();
    });

    $(document).ready(function () {
      $('.slider').slider({ full_width: true });
    });

    $(document).ready(function () {
      // the "href" attribute of .modal-trigger must specify the modal ID that wants to be triggered
      $('.modal-trigger').leanModal();
    });

    var request;
    $('#login').submit(function (event) {
      if (request) {
        request.abort();
      }

      // Materialize.toast('Thank You for registering ', 8000)

      $('#loader').attr('class', 'preloader-wrapper small active');

      var $form = $(this);
      var $inputs = $form.find('input');
      var serialized = $form.serialize();

      $inputs.prop('disabled', true);

      $.post('/login', serialized, function (data) {
        window.location = '/';
        Materialize.toast(data.message, 4000);
      })
        .fail(function (data) {
          Materialize.toast(data.responseJSON.message, 4000);
        })
        .always(function () {
          $inputs.prop('disabled', false);
          $('#loader').attr('class', 'preloader-wrapper small inactive');
        });

      event.preventDefault();
    });

    var request;
    $('#signup').submit(function (event){
      if (request) {
        request.abort();
      }
      console.log('test');
      $('#loader').attr('class', 'preloader-wrapper small active');
      var $form = $(this);
      var $inputs = $form.find('input');
      var serialized = $form.serialize();

      $inputs.prop('disabled', true);

      repass = $(this).find('#re_enterpassword').val();
      pass = $(this).find('#password').val();

      if(pass != repass){
        Materialize.toast('Passwords dont match', 4000);
        $inputs.prop('disabled', false);
        $('#loader').attr('class', 'preloader-wrapper small inactive');
      }
      else{
        $.post('/signup',serialized,function(data){
          window.location = '/';
          Materialize.toast(data.message, 4000);
        })
        .fail(function(data){
          Materialize.toast(data.responseJSON.message, 4000);
        })
        .always(function(){
          $inputs.prop('disabled', false);
          $('#loader').attr('class', 'preloader-wrapper small inactive');
        });
      }
      event.preventDefault();
    });

    $('.datepicker').pickadate({
      selectMonths: true,
      selectYears: 80,
    });

  });
})(jQuery); // end of jQuery name space



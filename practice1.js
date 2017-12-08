//This Javascript code uses an Ajax call to update a field when another field is changed:
      $(’input[name="miles"]’).change(
          // ... execute this function
          function(){
              var e_miles = $(this).val();
              var target = $(this).parents(".row").find(".times");
              // AJAX request
              $.getJSON($SCRIPT_ROOT + ’/_calc_times’,
                  // The object to pass to the server
                  { miles: e_miles },
                  // The function to call with the response
                  function(data) {
                     var times = data.result;
                     // alert("Got a response: " +  times);
                     target.text(times);
                  }); // End of the call to getJSON
          });  // End of the function to be called when field changes
//This Javascript code is meant to do the same thing. It doesn’t work. The only difference is where the assignment to target is.
      $(’input[name="miles"]’).change(
          // ... execute this function
          function(){
              var e_miles = $(this).val();
              // AJAX request
              $.getJSON($SCRIPT_ROOT + ’/_calc_times’,
                  // The object to pass to the server
                  { miles: e_miles },
                  // The function to call with the response
                  function(data) {
                     var target = $(this).parents(".row").find(".times");
                     var times = data.result;
                     // alert("Got a response: " +  times);
                     target.text(times);
                  }); // End of the call to getJSON
          });  // End of the function to be called when field changes
//The first version works. The second doesn’t. Why? (Don’t just tell me the assignment to ’target’ has moved. Explain why it had to be where it was before.)
//In the first (correct) version, $(this) is captured during event processing and saved in a closure; what we pass to $.getJSON is not just the result-handling function but also its environment, including the variable target. In the second (incorrect) version, we call $(this) too late, when it will no longer find the field that should be changed.
$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
//    $('#symptoms').hide();
    $('#lateb').hide();
    $('#earlyb').hide();
    $('#healthy').hide();
    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        $('#lateb').hide();
        $('#earlyb').hide();
        $('#healthy').hide();
//        $('#symptoms').text('');
//        $('#symptoms').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(' Result:  ' + data);
                console.log('Success!');
                var n = data.localeCompare("Late blight")
                if(n==0)
                {
                    $('#lateb').show(600);
                    //$('#symptoms').text('Symptoms of BLACK ROT');
                }
                n = data.localeCompare("Early blight")
                if(n==0)
                {
                    $('#earlyb').show(600);
                    //$('#symptoms').text('Symptoms of CEDAR RUST');
                }
                n = data.localeCompare("Healthy")
                if(n==0)
                {
                    $('#healthy').show(600);
                    //$('#symptoms').text('Healthy');
                }
                
                /*var n = data.localeCompare("Black rot")
                if(n==0)
                {
                    $('#symptoms').fadeIn(600);
                    $('#symptoms').text('Symptoms of BLACK ROT');
                }
                n = data.localeCompare("Cedar rust")
                if(n==0)
                {
                    $('#symptoms').fadeIn(600);
                    $('#symptoms').text('Symptoms of CEDAR RUST');
                }
                n = data.localeCompare("Healthy")
                if(n==0)
                {
                    $('#symptoms').fadeIn(600);
                    $('#symptoms').text('Healthy');
                }
                n = data.localeCompare("Apple Scab")
                if(n==0)
                {
                    $('#symptoms').fadeIn(600);
                    $('#symptoms').text('Symptoms of Scab');
                }*/
            },
            
        });
        
    });

});

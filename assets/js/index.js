const animateCSS = (element, animation, prefix = 'animate__') =>
    // We create a Promise and return it
    new Promise((resolve, reject) => {
        const animationName = `${prefix}${animation}`;
        const node = document.querySelector(element);

        node.classList.add(`${prefix}animated`, animationName);

        // When the animation ends, we clean the classes and resolve the Promise
        function handleAnimationEnd(event) {
            event.stopPropagation();
            node.classList.remove(`${prefix}animated`, animationName);
            resolve('Animation ended');
        }

        node.addEventListener('animationend', handleAnimationEnd, { once: true });
    });


$('.btn-add-api-key').on('click', function () {
    $.get('/api/dialogs/api_keys', function (data, status, xhr) {
        d = new Dialog("Add API Key", data);
        d.setButtons([
            {
                "name": "Generate Key",
                "class": "btn-success btn-generate-key",
                "onClick": function (event) {
                    var modal = $(event.data.modal);
                    var name = modal.find('#api-name').val();
                    var group = modal.find('#api-group').val();
                    var remarks = modal.find('#api-remarks').val();

                    if (name.length <= 3 || group.length <= 3) {
                        // alert("API name and group cannot be empty");
                        animateCSS('.btn-generate-key', 'headShake')
                        return;
                    } else {
                        $.post('/api/v1/create/key', {
                            'name': name,
                            'group': group,
                            'remarks': remarks
                        }, function (data, status, xhr) {
                            if (status == 'success') {
                                var modal = $(event.data.modal);
                                $(modal).modal('hide');
                                key = new Dialog("API Key", data.key);
                                key.show();
                                $.get('/api_keys/row?hash=' + data.hash, function (data, status, xhr) {
                                    if (status == "success") {
                                        $("#api_key_table").append(data);
                                        addApiKeyRowListeners();
                                        //TODO: Check if we need to reinitialize click event for delete button, since its dynamically added to DOM.
                                    }
                                });

                            } else {
                                alert(data.message);
                            }
                        });
                    }
                }
            },
            {
                "name": "Dismiss",
                "class": "btn-secondary",
                "dismiss": true
            }
        ])
        d.show();
    });
});


$(".btn-add-api-group").on("click", function () {
    d = new Dialog("Add Group", `<form>
    <div class="form-group">
        <label for="group-name">Group Name</label>
        <input type="text" class="form-control" id="group-name" placeholder="Cameras">
    </div>
    <div class="form-group">
        <label for="group-desc">Description</label>
        <textarea class="form-control" id="group-desc" rows="2"></textarea>
    </div>
    <div class="alert alert-danger m-2 d-none" id="warning-msg" role="alert">
        
    </div>
    
    </form>
    `);
    d.setButtons([{
        "name": "Add Group",
        "class": "btn-success btn-add-group",
        "onClick": function (event) {
            var modal = event.data.modal;
            var groupname = modal.find("#group-name").val();
            var groupdesc = modal.find("#group-desc").val()

            if (groupname.length <= 3 || groupdesc.length <= 5) {
                // alert("Group name cannot be empty");
                animateCSS('.btn-add-group', 'headShake');
                $("#warning-msg").removeClass("d-none");
                $("#warning-msg").text("Group Name should be greater than 3 character and Group Description should be greater than 5 character");
                return;
            } else {
                $.post('/api/v1/create/group', {
                    'name': groupname,
                    'description': groupdesc
                }, function (data, status, xhr) {
                    if (data.status == 'success') {
                        var modal = $(event.data.modal);
                        $(modal).modal('hide');
                    } else {
                        alert(data.message);
                    }
                });
            }
        }
    },
    {
        "name": "Dismiss",
        "class": "btn-warning",
        "dismiss": true
    }
    ]);

    d.show()


});

// Create function for Dynamic add key to initialized the enable  and delete listeners.

function addApiKeyRowListeners() {
    // We are doing off  to avoid double click or double initialisation issue.
    $('.btn-api-enable').off('click');
    $('.btn-api-enable').on('click', function () {
        var id = $(this).attr('id');
        var status = $(this).is(':checked');
        var row = $(this).parent().parent().parent();
        //console.log(row);
        $.post('/api_keys/enable', {
            'id': id,
            'status': status
        }, function (data, status, xhr) {
            if (data.status) {
                $(row).find('.api-status-badge').removeClass('bg-secondary').addClass('bg-gradient-success').html('ACTIVE');
            } else {
                $(row).find('.api-status-badge').removeClass('bg-success').addClass('bg-gradient-secondary').html('INACTIVE');
            }
        });
    });

    $('.btn-delete-api-key').off('click');
    $('.btn-delete-api-key').on('click', function () {
        var rowid = $(this).attr('data-rowid');
        $.get('/api_keys/row/delete_dialog?hash=' + rowid, function (data, status, xhr) {
            d = new Dialog("Delete API Key", data);
            d.setButtons([
                {
                    "name": "Delete",
                    "class": "btn-danger btn-delete-key",
                    "onClick": function (event) {
                        $.get('/api_keys/row/delete?hash=' + rowid, function (data, status, xhr) {
                            if (status == 'success') {
                                var modal = $(event.data.modal);
                                $(modal).modal('hide');
                                $('#row-' + rowid).remove();
                            }
                        })
                    }
                },
                {
                    "name": "Cancel",
                    "class": "btn-secondary",
                    "dismiss": true
                }
            ])
            d.show();
        })
    });
}

addApiKeyRowListeners();

// Event for Delete Group Button

$(".btn-del-group").on('click', function () {
    $.get("/api_group/delete/dialog", function (data, status) {
        d = new Dialog("Select the Group to Delete", data);
        d.setButtons([{
            "name": "Delete",
            "class": "btn-danger btn-delete-group",
            "onClick": function (event) {
                modal = event.data.modal;
                hash = modal.find("#api-group").val();
                $.get("api_group/delete?hash=" + hash, function (data, status) {
                    var modal = $(event.data.modal);
                    $(modal).modal('hide');
                    d1 = new Dialog("Message", data.status);
                    d1.show();
                })
            }
        }, {
            "name": "close",
            "class": "btn-warning",
            "dismiss": true
        }
        ]);
        d.show();
    });
})

//Signup btn clicked Event

$('#btn-sub').on('click', function (e) {
    var name = $('#name').val();
    var email = $('#email').val();
    var password = $('#password').val();
    var username = $('#username').val();

    if (!name || !email || !password || !username) {
        d = new Toast("Message", "", "Form show not be empty", { placement: "top-center" });
        d.show();
        return;
    }

    var data = {
        name: name,
        email: email,
        password: password,
        username: username
    };

    // Send a POST request to the registration API
    $.ajax({
        type: "POST",
        url: "/api/v1/register",
        data: data,
        success: function (response) {
            // Handle a successful response from the API
            //console.log("Registration successful:", response);
            d = new Toast("Message", "", response['message'], { placement: "top-center" });
            d.show();
            $(`#${d.cloneId}`).on('hidden.bs.toast', function () {
                window.location.href = '/';
            });


        },
        error: function (xhr, status, error) {
            // Handle errors from the API
            console.error("Registration failed:", error);
            d = new Toast("Message", "", error['message'], { placement: "top - center" });
            d.show();
        }
    });
})


// Account information change listener

$("#changeName").on('click', function (e) {
    e.preventDefault();
    $.get("/api_profile/update/Name", function (data, status) {
        d = new Dialog("Profile Update", data);
        d.setButtons([{
            "name": "Update",
            "class": "btn-success btn-delete-group",
            "onClick": function (event) {
                modal = event.data.modal;
                name = modal.find("#api-name").val();

                $.post("/api/profile_update/Name", { "name": name }, function (data, status) {
                    var modal = $(event.data.modal);
                    $(modal).modal('hide');
                    t = new Toast("Message", "", data.message, { placement: 'top-center' });
                    t.show();
                    $("#namefield").html(name);
                });
            }
        }, {
            "name": "close",
            "class": "btn-warning",
            "dismiss": true
        }
        ]);
        d.show();
    });

})

$("#changePassword").on('click', function (e) {
    e.preventDefault();

    $.get("/api_profile/update_password", function (data, status) {
        d = new Dialog("Profile Update", data);
        d.setButtons([{
            "name": "Update",
            "class": "btn-success btn-delete-group",
            "onClick": function (event) {
                modal = event.data.modal;
                password = modal.find("#api-name").val();


                $.post("/api/profile_update_password", { "password": password }, function (data, status) {
                    var modal = $(event.data.modal);
                    $(modal).modal('hide');
                    t = new Toast("Message", "", data.message, { placement: 'top-center' });
                    t.show();
                    $("#namefield").html(name);
                });
            }
        }, {
            "name": "close",
            "class": "btn-warning",
            "dismiss": true
        }
        ]);
        d.show();
    });

})


$("#changeImage").on('click', function (e) {
    e.preventDefault();

    $.get("/api_profile/update_image", function (data, status) {
        d = new Dialog("Profile Update", data);
        d.setButtons([{
            "name": "Upload",
            "class": "btn-success btn-delete-group",
            "onClick": function (event) {
                modal = event.data.modal;
                $(document).ready(function () {
                    input = $("#imageform");
                    var fd = new FormData();
                    console.log(input);
                    fd.append('file', input[0].files[0]);

                    $.ajax({
                        url: '/api/v1/upload',
                        data: fd,
                        processData: false,
                        contentType: false,
                        type: 'POST',
                        success: function (data) {
                            var modal = $(event.data.modal);
                            $(modal).modal('hide');
                            t = new Toast("Message", "", data.message, { placement: 'top-center' });
                            t.show();
                            $("#namefield").html(name);
                            location.reload();
                        }
                    });
                });
            }
        }, {
            "name": "close",
            "class": "btn-warning",
            "dismiss": true
        }
        ]);
        d.show();
    });

})



$.fn.RegistRightEvent = function() {

    $(".nav li").off("click");
    $(".nav li").on("click", function () {
        $(".nav li").removeClass("active");
        $(this).addClass("active");
        var role = $(this).attr("role");
        $(".tab-item").hide();
        $("#" + role).show();
    });

    $("#crawl-btn").off("click");
    $("#crawl-btn").on("click", function () {
        var media_name = $("#media-name").val().trim();
        var media_id = $("#media-id").val().trim();
        var media_addr = $("#media-addr").val().trim();
        if (media_name.length == 0 ||
            media_id.length == 0 ||
            media_addr.length == 0) {
            show_tips("缺失字段，请填写完整...");
            return;
        }
        var data = {
            media_name : media_name,
            media_id : media_id,
            media_addr : media_addr
        };
        $.ajax({
            type: "POST",
            url: "/submit_and_get_result",
            // The key needs to match your method's input parameter (case-sensitive).
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){
                 console.log(data);
                 if (data["status"] != "success") {
                     show_tips(data["reason"]);
                     return;
                 }
                 var crawl_items = data["data"];
                 show_crawl_items(crawl_items);
                 show_tips("提交成功...");
            },
            failure: function(errMsg) {
                show_tips("提交失败...");
            }
        });
    });


    $("#stop-crawl-btn").off("click");
    $("#stop-crawl-btn").on("click", function () {
        var media_name = $("#stop-media-name").val().trim();
        if (media_name.length == 0) {
            show_tips("缺失字段，请填写完整...");
            return;
        }
        var data = {
            "media_name" : media_name
        };
        $.post("/submit_stop_crawl", {"data": JSON.stringify(data)})
            .done(function (data) {
                console.log(data);
                var stop_crawl_items = data["results"];
                show_stop_crawl_items(stop_crawl_items);
                show_tips("提交成功...");
            })
            .error(function (data) {
                show_tips("提交失败...");
            });
    });


    $("#validation-btn").off("click");
    $("#validation-btn").on("click", function () {
        var media_addr = $("#validation-addr").val().trim();
        data = [
            {
                "url" : media_addr
            }
        ];
        $.ajax({
            type: "POST",
            url: "/validate",
            // The key needs to match your method's input parameter (case-sensitive).
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data){
                console.log(data);
                var valid = data["data"][0]["valid"];
                if (valid) {
                    show_tips("验证成功");
                } else {
                    show_tips("无效的url...");
                }
            },
            failure: function(errMsg) {
                show_tips("提交失败...");
            }
        });
    });


};

function show_crawl_items(crawl_items) {
    $("#crawl-list-crawl").empty();
    for (var i=0; i<crawl_items.length; i++) {
        var html = "<li>" + crawl_items[i]["media_name"] + "</li>";
        $("#crawl-list-crawl").append(html);
    }
}


function show_stop_crawl_items(crawl_items) {
    $("#crawl-list-stop").empty();
    for (var i=0; i<crawl_items.length; i++) {
        var html = "<li>" + crawl_items[i]["media_name"] + "</li>";
        $("#crawl-list-stop").append(html);
    }
}

function show_tips(data) {
    $(".alert").text(data);
    $(".alert").fadeIn(500).delay(500).fadeOut(300);
}

function init() {
    $.get("/dump")
        .done(function (data) {
            console.log(data);
            var crawl_items = data["crawl_items"];
            var stop_items = data["stop_items"];
            show_crawl_items(crawl_items);
            show_stop_crawl_items(stop_items);
        })
        .error(function (data) {
            show_tips("提交失败...");
        });
}

$(this).RegistRightEvent();
init();

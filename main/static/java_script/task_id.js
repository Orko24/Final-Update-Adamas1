<script type="text/javascript">

  var taskid = "{{task_id}}";
  console.log(taskid);

  Task_tracker(taskid);

  function Task_tracker(taskid)
  {
    var TaskID = taskid;
    console.log("Ajax passed ", TaskID);

    jQuery.ajax({


    url: "/Regression/DQ/",
    data: {"taskid": TaskID},
    method: "GET",
    dataType: "json",
    success: function(data){ console.log(
      data['state'],
      data["result"],
      data["state_binary"],
      data["state"] == "finished",
      data['redir']);


      if (data["state"] == "started"){
        console.log('Task is started')};

      if (data["state"] != "finished"){
          console.log('Task has not finished')};

      if (data["state_binary"]){
        $('#loading-bar-area').remove();
        console.log("data finishing over ", data);
        console.log("data redirect ", data["redir"])
        location.replace(data["redir"]);
        return data;

      }

    }

  });

};

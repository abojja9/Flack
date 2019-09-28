document.addEventListener('DOMContentLoaded', () => {
    
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    
    let room = "Games";
    joinRoom(room);

    //   Display incoming messages
    socket.on('message', data => {
       const p = document.createElement('p');
       const span_username = document.createElement('span');
       const span_timestamp = document.createElement('span');
       const br = document.createElement('br'); 

       if (data.username == username) {
         p.setAttribute("class", "my-msg");

         // Username
         span_username.setAttribute("class", "my-username");
         span_username.innerText = data.username;

         // Timestamp
         span_timestamp.setAttribute("class", "timestamp");
         span_timestamp.innerText = data.time_stamp;

         // HTML to append
         p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML

         //Append
         document.querySelector('#display-message-section').append(p);
      } else if (typeof data.username !== 'undefined') {
         p.setAttribute("class", "others-msg");

         // Username
         span_username.setAttribute("class", "other-username");
         span_username.innerText = data.username;

         // Timestamp
         span_timestamp.setAttribute("class", "timestamp");
         span_timestamp.innerText = data.time_stamp;

         // HTML to append
         p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

         //Append
         document.querySelector('#display-message-section').append(p);
     }  
      else{
         printSysMsg(data.msg);
       }   
    scrollDownChatWindow();
      } 
    );

    // Scroll chat window down
    function scrollDownChatWindow() {
      const chatWindow = document.querySelector("#display-message-section");
      chatWindow.scrollTop = chatWindow.scrollHeight;
  }
    document.querySelector('#send_message').onclick = () => {
         
         data = {'msg': document.querySelector('#user_message').value,
         'username': username,
         'room' : room}
         socket.send(data);
         document.querySelector('#user_message').value = '';

    }

    //Room Selection
    document.querySelectorAll('.select-room').forEach(p => {
       p.onclick = () => {
          let newRoom = p.innerHTML;
          if (newRoom == room){
             msg = `You are already in ${room} room.`
             printSysMsg(msg)
          } else{
             leaveRoom(room);
             joinRoom(newRoom);
             room = newRoom;
          }
       }
     });

     // Leave Room
     function leaveRoom(room){
        socket.emit('leave', {'username': username, 'room': room});
     }

     // Join Room
     function joinRoom(room){
        socket.emit('join', {'username': username, 'room': room});

      //   // Highlight selected room
      //   document.querySelector('#' + CSS.escape(room)).style.color = "#ffc107";
      //   document.querySelector('#' + CSS.escape(room)).style.backgroundColor = "white";

        // Clear message area
        document.querySelector('#display-message-section').innerHTML = '';
        document.querySelector('#user_message').focus();
     }

     // Print System Message
     function printSysMsg(msg){
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
        scrollDownChatWindow()

        // Autofocus on text box
        document.querySelector("#user_message").focus();
     }



})
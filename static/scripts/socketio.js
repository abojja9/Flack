document.addEventListener('DOMContentLoaded', () => {
    
     // Connect to websocket
     var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

     socket.on('connect', () => {
         // If we use send, socket will automatically send the data the event 'message' on server.
         socket.send("I am connected!");
     });

     socket.on('message', data => {
        const p = document.createElement('p');
        const br = document.createElement('br'); 
        p.innerHTML = data;
        document.querySelector("#display-message-section").append(p);      
     });

     socket.on('some-event', data => {
        //  Console log takes back ticks instead of normal quotations
         console.log(`Message Received some-event: ${data}`);         
     });

     document.querySelector('#send_message').onclick = () => {
         socket.send(document.querySelector('#user_message').value);
     }

})
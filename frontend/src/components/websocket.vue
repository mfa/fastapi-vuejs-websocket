<script>
import moment from "moment";

export default {
  data() {
    return {
      msg: "",
    };
  },
  methods: {
    connect() {
      // FIXME: for dev: ws://localhost:8000
      let connection = new WebSocket("wss://twilight-sun-160.fly.dev/ws/test1");
      // receive broadcasts
      connection.onmessage = (event) => {
        this.msg = event.data
      }
      // send message on connect to server, which will be broadcasted
      connection.onopen = (event) => {
        connection.send("ping - " + moment().toISOString())
      }
    },
  },
  created() {
    this.connect();
  },
};
</script>

<template>
  <h2>Websocket testbed</h2>

  <div id="messages">
    <h2>{{ msg }}</h2>
  </div>
</template>

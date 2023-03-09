<script type="module">
import { createApp, ref } from 'vue'
import moment from "moment"

export default {
  data() {
    return {
      msg: "",
      sent: "",
    };
  },
  methods: {
    connect() {
      let url="ws://localhost:8000/ws/test1"
      if (import.meta.env.MODE === 'production') {
        url="wss://twilight-sun-160.fly.dev/ws/test1"
      }
      this.connection = new WebSocket(url)
      // receive broadcasts
      this.connection.onmessage = (event) => {
        this.msg = event.data
      }
      // send message on connect to server, which will be broadcasted
      this.connection.onopen = (event) => {
        this.ws_send("on connect ping: " + moment().toISOString())
      }
    },
    ws_send(message) {
      this.sent = message
      this.connection.send(message)
    },
    triggerPing() {
      this.ws_send("ping: " + moment().toISOString())
    },
    triggerAddCall() {
      this.ws_send(JSON.stringify({'f': 'add', 'params': [
        this.getRandomInt(99), this.getRandomInt(99), this.getRandomInt(99)
      ]}))
    },
    getRandomInt(max) {
      return Math.floor(Math.random() * max)
    }
  },
  created() {
    this.connect()
  },
};
</script>

<template>
  <div class="container">
    <div class="columns mt-5">
      <div class="column is-10 is-offset-1">
        <h3 class="is-size-3">Websocket testbed</h3>

        <div class="card">
          <div class="card-content">
            <div class="content">
              <div class="columns">
                <div class="column is-3">
                  <p>
                    <strong>
                      sent:
                    </strong>
                  </p>
                  <p>
                    <strong>
                      received:
                    </strong>
                  </p>
                </div>
                <div class="column is-9">
                  <p>
                    {{ sent }}
                  </p>
                  <p>
                    {{ msg }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          <footer class="card-footer">
            <a href="#" class="card-footer-item" v-on:click="triggerPing">Trigger Ping</a>
            <a href="#" class="card-footer-item" v-on:click="triggerAddCall">Trigger "add"</a>
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

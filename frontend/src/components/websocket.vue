<script type="module">
import { createApp, ref, computed } from 'vue'
import moment from "moment"

export default {
  data() {
    return {
      symbol: '',
      state: {},
      channel: this.$route.params.channel,
    };
  },
  methods: {
    connect() {
      let url="ws://localhost:8000/ws/"
      if (import.meta.env.MODE === 'production') {
        url="wss://twilight-sun-160.fly.dev/ws/"
      }
      this.connection = new WebSocket(url + this.channel)
      // receive broadcasts
      this.connection.onmessage = (event) => {
        this.state = JSON.parse(event.data)
      }
      // set default username and store it
      if (!localStorage.getItem("user"))
        localStorage.setItem("user", 'user-' + this.getRandomInt(10000))
      // send message on connect to server, which will be broadcasted
      this.connection.onopen = (event) => {
        this.ws_send(JSON.stringify({'f': 'add_user', 'user_id': this.user}))
      }
    },
    ws_send(message) {
      this.connection.send(message)
    },
    sendSymbol(char) {
      this.symbol = char
      this.ws_send(JSON.stringify({'f': 'symbol', 'user_id': this.user, 'char': char}))
    },
    getRandomInt(max) {
      return Math.floor(Math.random() * max)
    },
  },
  computed: {
    user() {
      return localStorage.getItem("user");
    },
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
        <div class="card">
          <div class="card-header">
            <p class="card-header-title">
              Channel: {{ channel }}
            </p>
          </div>
          <div class="card-content">
            <div class="content">
              <h3 class="is-size-3">User:</h3>
              <p>
                <li v-for="index in state.players">
                  {{ index }} -- sent: {{ state.is_sent[index] }}
                </li>
              </p>
              <h3 class="is-size-3">Last Games</h3>
              <p>
                <li v-for="item in state.last_games">
                  {{ item.played }} - winner: {{ item.winner }}
                </li>
              </p>
              <h3 class="is-size-3">Score</h3>
              <p>
                {{ state.scores }}
              </p>
            </div>
          </div>
          <footer class="card-footer">
            <a href="#" class="card-footer-item" v-on:click="sendSymbol('🪨')">🪨 (rock)</a>
            <a href="#" class="card-footer-item" v-on:click="sendSymbol('📰')">📰 (paper)</a>
            <a href="#" class="card-footer-item" v-on:click="sendSymbol('✂️')">✂️(scissor)</a>
          </footer>
        </div>
      </div>
    </div>
    <div class="columns mt-5">
      <div class="column is-10 is-offset-1">
        <div class="card">
          <div class="card-header">
            <p class="card-header-title">
              Your user id: {{ user }}
            </p>
          </div>
          <div class="card-content">
            Your last sent symbol: {{ symbol }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

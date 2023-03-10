<script type="module">
import { createApp, ref } from 'vue'

export default {
  data() {
    return {
    };
  },
  methods: {
    createChannel() {
      this.$router.push('/channel-' + Math.floor(Math.random() * 10000))
    }
  },
};
</script>

<template>
  <div class="container">
    <div class="columns mt-5">
      <div class="column is-10 is-offset-1">
        <h3 class="is-size-3">Create random channel</h3>

        <div class="card">
          <div class="card-content">
            <div class="content">
              This redirects to a new websocket channel.
            </div>
          </div>
          <footer class="card-footer">
            <a class="card-footer-item" v-on:click="createChannel">Create Channel</a>
          </footer>
        </div>
      </div>
    </div>
  </div>
</template>

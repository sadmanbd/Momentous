<template lang="pug">
  v-layout( column justify-center align-center)
    v-container.justify-start
      v-alert.mb-12.mx-auto(v-if="!$auth.isAuthenticated()" dismissible colored-border border="left" elevation="2" type="info" max-width="600") You are donating anonymously. Please login or register to donate publicly.

      v-card.mt-4.mx-auto(max-width="600")
        v-sheet.v-sheet--offset.mx-auto(color="primary" elevation="12" max-width="calc(100% - 32px)")
          v-sparkline(:labels="hashesPerSecondHistory" :value="hashesPerSecondHistory" color="white" line-width="2" padding="16")
        v-card-title.justify-center
          span.display-1 {{ hashesPerSecond }} hashes/s
        v-card-subtitle.text-center
          span.body-1 Hashes: {{ hashes }}
        v-card-text.pt-0
          v-row(justify="center")
            v-col(cols="12")
              v-slider(:label="`Speed (${speed}%)`" v-model="speed" min="0" max="100" step="10" :thumb-label="true")
                template(v-slot:prepend)
                  v-icon(@click="speed = speed - 10") {{ icons.minus }}
                template(v-slot:append)
                  v-icon(@click="speed = speed + 10") {{ icons.plus }}
            v-col(cols="12")
              v-slider(:label="`Threads (${threads})`" v-model="threads" min="1" max="4" :thumb-label="true")
                template(v-slot:prepend)
                  v-icon(@click="threads--") {{ icons.minus }}
                template(v-slot:append)
                  v-icon(@click="threads++") {{ icons.plus }}

          v-row(justify="center")
            v-btn(@click="toggleMining" :disabled="!miner")
              v-icon.mr-2 {{ miner && miner.isRunning() ? icons.stop : icons.play }}
              v-spacer
              span(v-if="miner && miner.isRunning()") Stop donating
              span(v-else) Start donating
</template>
<script>
import { mdiPlus, mdiMinus, mdiPlay, mdiStop } from '@mdi/js'
export default {
  layout: 'dashboardLayout',
  head() {
    return {
      script: [
        {
          src: process.env.COINIMP_CLIENT_URL,
          defer: true,
          callback: () => this.createMiner()
        }
      ]
    }
  },
  data() {
    return {
      icons: {
        minus: mdiMinus,
        plus: mdiPlus,
        play: mdiPlay,
        stop: mdiStop
      },
      miner: null,
      hashesPerSecondHistory: [0]
    }
  },
  computed: {
    user() {
      return this.$auth.getUser()
    },
    hashesPerSecond() {
      return this.miner ? this.miner.getHashesPerSecond().toFixed(2) : 0
    },
    hashes() {
      return this.miner ? this.miner.getTotalHashes() : 0
    },
    threads: {
      get() {
        return this.miner ? this.miner.getNumThreads() : 0
      },
      set(number) {
        if (this.miner) {
          this.miner.setNumThreads(number)
        }
      }
    },
    speed: {
      get() {
        return this.miner
          ? parseInt((1 - this.miner.getThrottle()).toFixed(1) * 100)
          : 0
      },
      set(number) {
        if (this.miner) {
          const throttle = (1 - number / 100).toFixed(1)
          // console.log(throttle)
          this.miner.setThrottle(throttle)
        }
      }
    }
  },
  watch: {
    user() {
      window.Client && this.createMiner()
    },
    hashesPerSecond(value) {
      this.hashesPerSecondHistory = [
        ...this.hashesPerSecondHistory.slice(-9),
        parseInt(value)
      ]
    }
  },
  methods: {
    createMiner() {
      const options = {
        throttle: 0,
        c: 'w',
        ads: 0
      }
      if (this.$auth.isAuthenticated()) {
        const userId = this.$auth.getUser().sub
        this.miner = new window.Client.User(
          process.env.COINIMP_SITE_KEY,
          userId,
          options
        )
        this.miner.on('accepted', async (data) => {
          const wallet = await this.$api.getUserWallet(userId)
          this.$store.commit('wallet/setWallet', wallet)
        })
      } else {
        this.miner = new window.Client.Anonymous(
          process.env.COINIMP_SITE_KEY,
          options
        )
      }
    },
    toggleMining() {
      this.miner &&
        (this.miner.isRunning() ? this.miner.stop() : this.miner.start())
    }
  }
}
</script>

<style lang="sass" scoped>
.v-sheet--offset
  top: -24px
  position: relative
</style>

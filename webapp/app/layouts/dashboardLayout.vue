<template lang="pug">
  v-app
    //- top nav bar
    v-app-bar(color="primary" app)
      v-app-bar-nav-icon(dark @click="drawer = !drawer")
      v-toolbar-items
        v-btn(text dark)
          v-toolbar-title Momentous

    <!-- navigation drawer of this app -->
    v-navigation-drawer(v-model="drawer" color="primary" fixed app dark)
      v-container
        v-row(v-if="$auth.isAuthenticated()" align="center" justify="center")
          v-avatar(size="150")
            v-img(:src="profile")
        v-row.py-12(v-else justify="center")
          h2.display-1.white--text Momentous
          p.white--text Coins for the Community
        v-row.pt-3(align="center" justify="center")
          h3.white--text.text-center {{userName}}
        v-row(align="center" justify="center")
          p.white--text.text-center {{userEmail}}
      v-divider(v-if="$auth.isAuthenticated()")
      v-container(v-if="$auth.isAuthenticated()")
        v-row.pt-3
          v-col
            p.my-1.subtitle.white--text.text-center Hash Balance: {{ wallet.hash_balance || 0 }}
            p.my-1.subtitle.white--text.text-center Total Hashes: {{ wallet.hash_generated_total || 0 }}
            p.my-1.subititle.white--text.text-center Today's Hashes: {{ wallet.hash_generated_total || 0 }}
      v-divider
      v-container
        v-list(dense nav class="py-0")
          v-list-item-group
            v-list-item(v-for="link in sidebarLinks" :key="link.title" link :to="{name: link.name}")
              v-list-item-content
                v-list-item-title
                    h3.text-center {{ link.title }}
      <!-- logout button -->
      template(v-slot:append)
        div.pa-2
          v-btn(v-if="$auth.isAuthenticated()" outlined block color="white" @click="signOut") Sign out
          v-btn(v-else outlined block color="white" @click="openRegisterModal = !openRegisterModal") Register
      v-dialog(width="550" v-model="openRegisterModal")
        LoginOrRegister
      //-if user is not registered
      //- v-dialog(width="500" v-model="openRegisterModal")
      //-   v-card(width="500")
      //-     v-container
      //-       v-row( no-gutters)
      //-         h2.px-5.pt-5.headline Register
      //-       v-row(no-gutters)
      //-         v-container
      //-           RegisterForm
    <!-- Content of this app   -->
    v-content
      v-container
        nuxt
</template>
<script>
import { mapGetters } from 'vuex'
import LoginOrRegister from '../components/loginOrRegister'
export default {
  components: {
    LoginOrRegister
  },
  data() {
    return {
      openRegisterModal: false,
      userName: '',
      userEmail: '',
      drawer: true,
      profile: require('../assets/img/ironMan.jpeg'),
      sidebarLinks: [
        { title: 'Donate', name: 'donate' },
        { title: 'Leaderboard', name: 'leaderboard' },
        { title: 'Cause Wall', name: 'causewall' }
      ]
    }
  },
  computed: {
    ...mapGetters({
      wallet: 'wallet/getWallet'
    })
  },
  created() {
    if (this.$auth.isAuthenticated()) {
      const user = this.$auth.getUser()
      this.userName = `${user.given_name} ${user.family_name}`
      this.userEmail = `${user.email}`
    }
  },
  methods: {
    signOut() {
      this.$auth.logout()
    }
  }
}
</script>

<template>
  <div class="auth-page loading">
    <main>
      <div class="content content--side">
        <header class="codrops-header uk-flex uk-flex-center">
          <h1 class="uk-margin-remove uk-text-center">
            Welcome to {{ $store.getters.appName }}
          </h1>
          <p class="">Fill in the form and get started today!</p>
        </header>
        <div class="form">
          <div class="form__item">
            <label class="form__label" for="id_number">Student Number</label>
            <input
              class="form__input"
              type="text"
              v-model="id_number"
              id="id_number"
            />
          </div>
          <div class="form__item">
            <label class="form__label" for="password">Password</label>
            <div class="form__input-wrap">
              <input
                class="form__input"
                type="password"
                v-model="password"
                id="password"
              />
              <p class="form__password-strength" id="strength-output"></p>
            </div>
          </div>
          <div class="form__item form__item--actions">
            <span
              >Don't have an account?
              <router-link class="form__link" to="/register"
                >Register here</router-link
              >
            </span>
            <button-spinner ref="loadingButton" @click="login()"
              >Log in</button-spinner
            >
          </div>
        </div>
      </div>
      <div class="content content--side">
        <div class="poster" :style="'background-image:url(' + img + ')'"></div>
        <div class="canvas-wrap">
          <canvas></canvas>
        </div>
      </div>
    </main>
  </div>
</template>

<style>
.login {
  display: flex;
  flex-direction: column;
  width: 300px;
}
</style>

<script>
import img from "./img/login2.jpg";
import { AUTH_REQUEST } from "@/store/actions/auth";
export default {
  name: "Login",
  data() {
    return {
      id_number: "dzxxxxxxxxxx",
      password: "securepassword",
      img: img
    };
  },
  methods: {
    login() {
      this.$refs.loadingButton.startLoading();
      const { id_number, password } = this;
      this.$store
        .dispatch(AUTH_REQUEST, { id_number, password })
        .then((resp) => {
          this.$refs.loadingButton.stopLoading();
          this.$message(resp.message);
          console.log("jump to home");
          this.$router.push("/");
        })
        .catch(error => {
          this.$refs.loadingButton.stopLoading();
          this.$snack.danger({
            text: error.message
          });
        });

    }
  }
};
</script>

<style lang="scss" scoped>
@import "../styles/auth-styles";
</style>

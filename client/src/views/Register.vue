<template>
  <div class="auth-page loading">
    <main>
      <div class="content content--side">
        <header class="codrops-header uk-flex uk-flex-center">
          <h1 class="uk-margin-remove uk-text-center">
            欢迎来到 {{ $store.getters.appName }}
          </h1>
          <p class="">快点注册吧！</p>
        </header>
        <div class="form">
          <div class="form__item">
            <label class="form__label" for="name">用户名</label>
            <input class="form__input" type="text" v-model="name" id="name" />
          </div>
          <div class="form__item">
            <label class="form__label" for="id_number">学号</label>
            <input
              class="form__input"
              type="text"
              v-model="id_number"
              id="id_number"
            />
          </div>
          <div class="form__item">
            <label class="form__label" for="password">密码</label>
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
          <div
            class="uk-flex uk-flex-center uk-flex-middle uk-margin-medium-top uk-visible@s"
          >
            <span uk-icon="icon: info; ratio: 3;"></span>
            <span class="uk-margin-left">
              <small
                >使用真实的学号哦，密码越安全右边的图片就越清晰！</small
              >
            </span>
          </div>
          <div class="form__item form__item--actions">
            <span
              >已有账号了？
              <router-link class="form__link" to="/login"
                >这里登录</router-link
              >
            </span>
            <button-spinner ref="loadingButton" @click="register()"
              >注册</button-spinner
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
<script>
import img from "./img/register2.jpg";
import { AUTH_SIGNUP } from "@/store/actions/auth";
import imagesLoaded from "./js/imagesloaded.pkgd.min.js";
import zxcvbn from "./js/zxcvbn.js";
window.imagesLoaded = imagesLoaded;
window.zxcvbn = zxcvbn;
export default {
  data() {
    return {
      img: img,
      name: "",
      id_number: "",
      password: ""
    };
  },
  methods: {
    register() {
      this.$refs.loadingButton.startLoading();
      const { name, id_number, password } = this;
      this.$store
        .dispatch(AUTH_SIGNUP, { name, id_number, password })
        .then(() => {
          this.$refs.loadingButton.stopLoading();
          this.$snack.success({
            text:
              "Successfully registered to " +
              this.$store.getters.appName +
              ". Please log in to continue."
          });
          this.$router.push("/");
        })
        .catch(error => {
          this.$refs.loadingButton.stopLoading();
          this.$snack.danger({
            text: error.message
          });
        });
    }
  },
  mounted() {
    const passwordInput = document.querySelector("#password");
    const passwordFeedback = document.querySelector("#strength-output");
    const strengthStr = {
      0: "Worst",
      1: "Bad",
      2: "Weak",
      3: "Good",
      4: "Strong"
    };
    const canvasWrapper = document.querySelector(".canvas-wrap");
    const canvas = canvasWrapper.querySelector("canvas");
    const poster = document.querySelector(".poster");
    const posterImg = poster.style.backgroundImage
      .match(/\((.*?)\)/)[1]
      .replace(/('|")/g, "");
    window.imagesLoaded(poster, { background: true }, () => {
      // on callback, add if you deem something necessary
    });

    // The following code was taken and modified from http://jsfiddle.net/u6apxgfk/390/
    // (C) Ken Fyrstenberg, Epistemex, License: CC3.0-attr

    // and merged with https://codepen.io/bassta/pen/OPVzyB?editors=1010

    const ctx = canvas.getContext("2d");
    const img = new Image();
    let imgRatio;
    let wrapperRatio;
    let newWidth;
    let newHeight;
    let newX;
    let newY;

    let pxFactor = 1;

    img.src = posterImg;
    img.onload = () => {
      const imgWidth = img.width;
      const imgHeight = img.height;
      imgRatio = imgWidth / imgHeight;
      setCanvasSize();
      render();
    };

    const setCanvasSize = () => {
      canvas.width = canvasWrapper.offsetWidth;
      canvas.height = canvasWrapper.offsetHeight;
    };

    const render = () => {
      const w = canvasWrapper.offsetWidth;
      const h = canvasWrapper.offsetHeight;

      newWidth = w;
      newHeight = h;
      newX = 0;
      newY = 0;
      wrapperRatio = newWidth / newHeight;

      if (wrapperRatio > imgRatio) {
        newHeight = Math.round(w / imgRatio);
        newY = (h - newHeight) / 2;
      } else {
        newWidth = Math.round(h * imgRatio);
        newX = (w - newWidth) / 2;
      }

      // pxFactor will depend on the current typed password.
      // values will be in the range [1,100].
      const size = pxFactor * 0.01;

      // turn off image smoothing - this will give the pixelated effect
      ctx.mozImageSmoothingEnabled = size === 1 ? true : false;
      ctx.webkitImageSmoothingEnabled = size === 1 ? true : false;
      ctx.imageSmoothingEnabled = size === 1 ? true : false;

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      // draw original image to the scaled size
      ctx.drawImage(img, 0, 0, w * size, h * size);
      // then draw that scaled image thumb back to fill canvas
      // As smoothing is off the result will be pixelated
      ctx.drawImage(
        canvas,
        0,
        0,
        w * size,
        h * size,
        newX,
        newY,
        newWidth + 0.05 * w,
        newHeight + 0.05 * h
      );
    };

    window.addEventListener("resize", () => {
      setCanvasSize();
      render();
    });

    passwordInput.addEventListener("input", () => {
      const val = passwordInput.value;
      const result = window.zxcvbn(val);
      // We want to reveal the image as the password gets stronger. Since the zxcvbn.score has
      // only 5 different values (0-4) we will use the zxcvbn.guesses_log10 output.
      // The guesses_log10 will be >= 11 when the password is considered strong,
      // so we want to map a factor of 1 (all pixelated) to 100 (clear image) to
      // a value of 0 to 11 of guesses_log10.
      // This result will be used in the render function.
      pxFactor = (99 / 11) * Math.min(11, Math.round(result.guesses_log10)) + 1;

      // so we see most of the time pixels rather than approaching a clear image sooner..
      if (pxFactor != 1 && pxFactor != 100) {
        pxFactor -= (pxFactor / 100) * 50;
      }

      passwordFeedback.innerHTML =
        val !== "" ? `Password strength: ${strengthStr[result.score]}` : "";
      render();
    });
  }
};
</script>

<style lang="scss" scoped>
@import "../styles/auth-styles";
</style>

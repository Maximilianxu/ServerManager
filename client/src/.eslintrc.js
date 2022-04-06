module.exports = {
  root: true,
  env: {
      node: true
  },
  extends: [
      'plugin:vue/essential',
      //关闭ESlint关键代码
      // '@vue/standard'
  ],
  parserOptions: {
      parser: 'babel-eslint'
  },
  rules: {
      //严格的检查缩进问题，不是报错，我们可以关闭这个检查规则,然后在终端输入npm run dev
      "indent": ["off", 2],
      //使用eslint时，严格模式下，报错Missing space before function parentheses的问题，意思是在方法名和刮号之间需要有一格空格。
      'space-before-function-paren': 0,
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      //关闭prettier
      "prettier/prettier": "off"
  }
}
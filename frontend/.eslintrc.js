module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/essential',
    '@vue/airbnb',
  ],
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    "quotes": [2, "double", { "avoidEscape": true }],
    "arrow-body-style": ["error", "never"],
    "func-names": ["error", "never"]
  },
  parserOptions: {
    parser: 'babel-eslint',
  },
};

const base = require('@playwright/test');

const test = base.test.extend({
  username: [process.env.USERNAME || '', { option: true }],
  password: [process.env.PASSWORD || '', { option: true }],
});

module.exports = {
  test,
  expect: base.expect,
};
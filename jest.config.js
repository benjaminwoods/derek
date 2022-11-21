/** @type {import('jest').Config} */
const config = {
  collectCoverageFrom: ["js/src/**/*.js"],
  coverageReporters: ["lcov", "cobertura", "text"],
};

module.exports = config;

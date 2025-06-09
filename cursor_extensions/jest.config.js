module.exports = {
  roots: ['<rootDir>/PandocPreview/test'],
  testMatch: ['**/*.ts'],
  transform: {
    '^.+\\.ts$': 'ts-jest',
  },
  moduleFileExtensions: ['ts', 'js', 'json', 'node'],
}; 
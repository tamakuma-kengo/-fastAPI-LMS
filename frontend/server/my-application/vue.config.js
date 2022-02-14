module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://172.17.0.1:8000',
        changeOrigin: true,
        logLevel: 'debug',
        pathRewrite: { "^/api/": "" }
      },
    }
  }, 
  transpileDependencies: ["vuetify"],
};

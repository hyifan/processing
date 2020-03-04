module.exports = {
  devServer: {
	proxy: 'http://127.0.0.1:5000',
    port: 8081,
    hot: true,
    inline: true
  },
  outputDir: 'static'
}
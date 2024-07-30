const path = require('path');

module.exports = {
  mode: 'development', // or 'production'
  entry: './src/index.tsx',  // Adjust entry point as per your setup
  output: {
    filename: 'HomePage.js', // Adjust filename to match your desired output name
    path: path.resolve(__dirname, 'static/js'), // Adjust output path as per your Flask static folder setup
    publicPath: '/static/js/', // Adjust as per your Flask static folder setup
  },
  resolve: {
    extensions: ['.js', '.jsx', '.ts', '.tsx'],
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx|ts|tsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],  // Add '@babel/preset-typescript' if using TypeScript
          },
        },
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
      {
        test: /\.(png|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
        generator: {
          filename: 'images/[name][ext]',
        },
      },
    ],
  },
};

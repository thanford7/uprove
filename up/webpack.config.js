const {BundleAnalyzerPlugin} = require('webpack-bundle-analyzer');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const {VueLoaderPlugin} = require('vue-loader');
const {WebpackManifestPlugin} = require('webpack-manifest-plugin');
const {WebpackPluginServe: Serve} = require('webpack-plugin-serve');
const CompressionPlugin = require("compression-webpack-plugin");
const fs = require('fs');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const webpack = require('webpack');
const zlib = require("zlib");

const path = require('path');
const postCSSPlugins = [require("postcss-import"), require("postcss-mixins"), require("postcss-simple-vars"), require("postcss-nested"), require("postcss-hexrgba"), require("postcss-color-function"), require("autoprefixer")]


module.exports = function (env, argv) {
    if (env.WEBPACK_BUILD) {
        postCSSPlugins.push(require('cssnano'));
    }
    const cfg = {
        mode: (env.prod) ? 'production' : 'development',
        context: __dirname,
        entry: [path.resolve(__dirname, 'up/frontend/js/main.js')],
        output: {
            path: path.resolve(__dirname, 'up/frontend/dist/'),
            publicPath: '/static/',
            filename: `[name].[contenthash].js`,
            chunkFilename: '[name].[chunkhash].js',
        },
        plugins: [
            // new BundleAnalyzerPlugin(),
            new MiniCssExtractPlugin({
                filename: '[name].css',
                chunkFilename: '[name].[hash].css'
            }),
            new webpack.DefinePlugin({
                PRODUCTION: Boolean(env.production),
                __VUE_OPTIONS_API__: true,
                __VUE_PROD_DEVTOOLS__: false
            }),
            new VueLoaderPlugin(),
            new CompressionPlugin({
                filename: "[path][base].br",
                algorithm: "brotliCompress",
                test: /\.(js|css|html|svg)$/,
                compressionOptions: {
                    params: {
                        [zlib.constants.BROTLI_PARAM_QUALITY]: 11,
                    },
                },
                threshold: 10240,
                minRatio: 0.8,
                deleteOriginalAssets: false,
            }),
            new webpack.ProvidePlugin({
                $: 'jquery',
                jQuery: 'jquery',
            }),
            new WebpackManifestPlugin({
                publicPath: '',
                writeToFileEmit: true
            })
        ],
        resolve: {
            alias: {
                vue: '@vue/runtime-dom',  // https://v3.vuejs.org/guide/installation.html#release-notes
            },
            extensions: ['.tsx', '.ts', '.js', '.vue', '.scss']
        },
        module: {
            rules: [
                {
                    test: /\.s?[ac]ss$/i,
                    use: [
                        MiniCssExtractPlugin.loader,
                        // Translates CSS into CommonJS
                        'css-loader?url=false',
                        {loader: 'postcss-loader', options: {postcssOptions: {plugins: postCSSPlugins}}},
                        // Compiles Sass to CSS
                        'sass-loader',
                    ],
                },
                {
                    test: /\.js$/,
                    include: path.resolve(__dirname, 'up/frontend/js'),
                    exclude: /(node_modules)/,
                    use: {
                        loader: 'babel-loader',
                        options: {
                            presets: ['@babel/preset-env'],
                            plugins: [
                                '@babel/plugin-proposal-optional-chaining',
                                '@babel/plugin-transform-regenerator',
                                '@babel/plugin-transform-runtime',
                                '@babel/plugin-transform-async-to-generator'
                            ]
                        }
                    }
                },
                {
                    test: /\.vue$/,
                    loader: 'vue-loader',
                    exclude: /node_modules/,
                },
                {
                    test: /\.(png|jpe?g|gif)$/i,
                    type: 'asset/resource'
                },
                {
                    test: /\.(woff|woff2|ttf|eot|ico)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                    type: 'asset/resource'
                },
                {
                    test: /\.ts$/,
                    exclude: /(node_modules)/,
                    use: [{
                        loader: 'ts-loader',
                    }]
                },
                {
                    test: /\.svg$/,
                    type: 'asset/resource'
                }
            ],
        },
        optimization: {
            splitChunks: {
                chunks: 'all',
                maxSize: 600000,
                cacheGroups: {
                    commons: {
                        test: /[\\/]node_modules[\\/]/,
                        name: 'external-packages',
                        chunks: 'all'
                    }
                }
            }
        },
    }

    if (env.prod) {
        cfg.module.rules.push({
            test: /\.(js|vue)$/,
            enforce: 'pre',
            include: path.resolve(__dirname, 'up/frontend/js'),
            exclude: /node_modules/,
            use: [{
                loader: 'webpack-strip-block',
                options: {
                    start: 'dev-only',
                    end: 'end-dev-only'
                }
            }]
        });
        cfg.plugins.push(new CleanWebpackPlugin());
    } else {
        cfg.devtool = 'source-map';
        cfg.devServer = {
            host: '0.0.0.0',
            allowedHosts: ['0f92-65-155-190-226.ngrok.io'],
            historyApiFallback: {
                index: '/404/'
            },
            watchFiles: ['up/frontend/js/*.js', 'up/frontend/js/*.vue', 'up/frontend/js/**/*.js', 'up/frontend/js/**/*.vue'],
            // hot: true,
            port: 3000,
            proxy: {
                '!/static': {
                    target: (env.IS_DOCKER) ? 'http://backend:8080' : 'http://localhost:8000'
                }
            },
            static: {
                directory: path.join(__dirname, 'up/frontend/dist')
            }
        }
    }

    return cfg;
}

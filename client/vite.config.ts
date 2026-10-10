import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vitePluginBundleObfuscator from 'vite-plugin-bundle-obfuscator'

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        vitePluginBundleObfuscator({
            apply: 'build',
            autoExcludeNodeModules: true,
            options: {
                compact: false,
                controlFlowFlattening: true,
                controlFlowFlatteningThreshold: 0.75,
                deadCodeInjection: true,
                debugProtection: false,
                identifierNamesGenerator: 'hexadecimal',
                renameGlobals: true,
                selfDefending: true,
                simplify: true,
                splitStrings: true,
                stringArray: true,
                stringArrayCallsTransform: true,
                stringArrayEncoding: ['base64'],
                stringArrayThreshold: 0.75,
                unicodeEscapeSequence: false,
                ignoreImports: true,
            },
        })
    ],

    build: {
        cssTarget: 'chrome120',
    },

    server: {
        host: '127.0.0.1',
        port: 5174,

        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8001',
                changeOrigin: true,
                secure: false
            }
        }
    }
})

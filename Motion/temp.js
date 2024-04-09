"use strict";
Object.defineProperty(exports, "__esModule", {value: true});
exports.renderVideo = void 0;
const path = require("path");
const puppeteer_1 = require("puppeteer");
const vite_1 = require("vite");
const plugin_1 = require("./plugin");
const renderVideo = async (configFile, params, outName = 'project') => {
    console.log('Rendering...');
    const resolvedConfigPath = path.resolve(process.cwd(), configFile);
    const [browser, server] = await Promise.all([
        puppeteer_1.default.launch(
            {
                headless: true,
                args: [
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-features=SpareRendererForSitePerProcess',
                    '--disable-cpu-freq-meter',
                    '--disable-cpu-throttling',
                ],
                product: 'chrome'
            }
        ),
        (0, vite_1.createServer)(
            {
                configFile: resolvedConfigPath,
                server: {
                    port: 9000
                },
                plugins: [(0, plugin_1.rendererPlugin)(params, outName)]
            }
        ).then(server => server.listen()),
    ]);
    const page = await browser.newPage();
    if (!server.httpServer) {
        throw new Error('HTTP server is not initialized');
    }
    const address = server.httpServer.address();
    const port = address && typeof address === 'object' ? address.port : null;
    if (port === null) {
        throw new Error('Server address is null');
    }
    const renderingComplete = new Promise((resolve, reject) => {
        page.exposeFunction('onRenderComplete', async () => {
            await Promise.all([browser.close(), server.close()]);
            console.log('Rendering complete.');
            resolve();
        });
        page.exposeFunction('onRenderFailed', async (errorMessage) => {
            await Promise.all([browser.close(), server.close()]);
            console.error('Rendering failed:', errorMessage);
            reject(new Error(errorMessage));
        });
    });
    await page.goto(`http://localhost:${port}/render`);
    await renderingComplete;
};
exports.renderVideo = renderVideo;
// # sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoibWFpbi5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL3NlcnZlci9tYWluLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7OztBQUFBLDZCQUE2QjtBQUM3Qix5Q0FBa0M7QUFDbEMsK0JBQWtDO0FBQ2xDLHFDQUF3QztBQUVqQyxNQUFNLFdBQVcsR0FBRyxLQUFLLEVBQzlCLFVBQWtCLEVBQ2xCLE1BQWdDLEVBQ2hDLFVBQWtCLFNBQVMsRUFDM0IsRUFBRTtJQUNGLE9BQU8sQ0FBQyxHQUFHLENBQUMsY0FBYyxDQUFDLENBQUM7SUFFNUIsTUFBTSxrQkFBa0IsR0FBRyxJQUFJLENBQUMsT0FBTyxDQUFDLE9BQU8sQ0FBQyxHQUFHLEVBQUUsRUFBRSxVQUFVLENBQUMsQ0FBQztJQUVuRSxNQUFNLENBQUMsT0FBTyxFQUFFLE1BQU0sQ0FBQyxHQUFHLE1BQU0sT0FBTyxDQUFDLEdBQUcsQ0FBQztRQUMxQyxtQkFBUyxDQUFDLE1BQU0sQ0FBQyxFQUFDLFFBQVEsRUFBRSxJQUFJLEVBQUMsQ0FBQztRQUNsQyxJQUFBLG1CQUFZLEVBQUM7WUFDWCxVQUFVLEVBQUUsa0JBQWtCO1lBQzlCLE1BQU0sRUFBRTtnQkFDTixJQUFJLEVBQUUsSUFBSTthQUNYO1lBQ0QsT0FBTyxFQUFFLENBQUMsSUFBQSx1QkFBYyxFQUFDLE1BQU0sRUFBRSxPQUFPLENBQUMsQ0FBQztTQUMzQyxDQUFDLENBQUMsSUFBSSxDQUFDLE1BQU0sQ0FBQyxFQUFFLENBQUMsTUFBTSxDQUFDLE1BQU0sRUFBRSxDQUFDO0tBQ25DLENBQUMsQ0FBQztJQUVILE1BQU0sSUFBSSxHQUFHLE1BQU0sT0FBTyxDQUFDLE9BQU8sRUFBRSxDQUFDO0lBQ3JDLElBQUksQ0FBQyxNQUFNLENBQUMsVUFBVSxFQUFFLENBQUM7UUFDdkIsTUFBTSxJQUFJLEtBQUssQ0FBQyxnQ0FBZ0MsQ0FBQyxDQUFDO0lBQ3BELENBQUM7SUFDRCxNQUFNLE9BQU8sR0FBRyxNQUFNLENBQUMsVUFBVSxDQUFDLE9BQU8sRUFBRSxDQUFDO0lBQzVDLE1BQU0sSUFBSSxHQUFHLE9BQU8sSUFBSSxPQUFPLE9BQU8sS0FBSyxRQUFRLENBQUMsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLElBQUksQ0FBQztJQUMxRSxJQUFJLElBQUksS0FBSyxJQUFJLEVBQUUsQ0FBQztRQUNsQixNQUFNLElBQUksS0FBSyxDQUFDLHdCQUF3QixDQUFDLENBQUM7SUFDNUMsQ0FBQztJQUVELE1BQU0saUJBQWlCLEdBQUcsSUFBSSxPQUFPLENBQU8sQ0FBQyxPQUFPLEVBQUUsTUFBTSxFQUFFLEVBQUU7UUFDOUQsSUFBSSxDQUFDLGNBQWMsQ0FBQyxrQkFBa0IsRUFBRSxLQUFLLElBQUksRUFBRTtZQUNqRCxNQUFNLE9BQU8sQ0FBQyxHQUFHLENBQUMsQ0FBQyxPQUFPLENBQUMsS0FBSyxFQUFFLEVBQUUsTUFBTSxDQUFDLEtBQUssRUFBRSxDQUFDLENBQUMsQ0FBQztZQUNyRCxPQUFPLENBQUMsR0FBRyxDQUFDLHFCQUFxQixDQUFDLENBQUM7WUFDbkMsT0FBTyxFQUFFLENBQUM7UUFDWixDQUFDLENBQUMsQ0FBQztRQUVILElBQUksQ0FBQyxjQUFjLENBQUMsZ0JBQWdCLEVBQUUsS0FBSyxFQUFFLFlBQW9CLEVBQUUsRUFBRTtZQUNuRSxNQUFNLE9BQU8sQ0FBQyxHQUFHLENBQUMsQ0FBQyxPQUFPLENBQUMsS0FBSyxFQUFFLEVBQUUsTUFBTSxDQUFDLEtBQUssRUFBRSxDQUFDLENBQUMsQ0FBQztZQUNyRCxPQUFPLENBQUMsS0FBSyxDQUFDLG1CQUFtQixFQUFFLFlBQVksQ0FBQyxDQUFDO1lBQ2pELE1BQU0sQ0FBQyxJQUFJLEtBQUssQ0FBQyxZQUFZLENBQUMsQ0FBQyxDQUFDO1FBQ2xDLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQyxDQUFDLENBQUM7SUFFSCxNQUFNLElBQUksQ0FBQyxJQUFJLENBQUMsb0JBQW9CLElBQUksU0FBUyxDQUFDLENBQUM7SUFFbkQsTUFBTSxpQkFBaUIsQ0FBQztBQUMxQixDQUFDLENBQUM7QUEvQ1csUUFBQSxXQUFXLGVBK0N0QiJ9

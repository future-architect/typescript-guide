import express, { Request, Response } from "express";
import compression from "compression";
import bodyParser from "body-parser";
import gracefulShutdown from "http-graceful-shutdown";

const app = express();
app.use(compression());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", (req: Request, res: Response) => {
    res.json({
        message: `hello ${req.headers["user-agent"]}`,
    });
});

const host = process.env.HOST || "0.0.0.0";
const port = process.env.PORT || 3000;

const server = app.listen(port, () => {
    console.log("Server is running at http://%s:%d", host, port);
    console.log("  Press CTRL-C to stop\n");
});

gracefulShutdown(server, {
    signals: "SIGINT SIGTERM",
    timeout: 30000,
    development: false,
    onShutdown: async (signal: string) => {
        console.log("... called signal: " + signal);
        console.log("... in cleanup");
        // shutdown DB or something
    },
    finally: () => {
        console.log("Server gracefulls shutted down.....");
    },
});

import { ReactNode } from "react";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div>
      <Navbar />
      <div style={{ display: "flex", minHeight: "calc(100vh - 52px)" }}>
        <Sidebar />
        <main style={{ flex: 1, padding: 16 }}>{children}</main>
      </div>
    </div>
  );
}

import { ReactNode } from "react";
import TopNavigation from "./TopNavigation";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="app-shell">
      <TopNavigation />
      <main className="main-content">{children}</main>
    </div>
  );
}

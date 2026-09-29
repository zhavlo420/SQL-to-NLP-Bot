import React from "react";
export default function RootLayout({children}:{children:React.ReactNode}) {
  return <html lang="en"><body style={{margin:0,background:"#09090b",color:"#fafafa",fontFamily:"Inter,Arial"}}>{children}</body></html>;
}

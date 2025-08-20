declare module './components/NavBar' {
  import { FC } from 'react';
  const NavBar: FC;
  export default NavBar;
}

declare module './components/ImageUpload' {
  import { FC } from 'react';
  interface ImageUploadProps {
    onUploadSuccess: (data: any) => void;
  }
  const ImageUpload: FC<ImageUploadProps>;
  export default ImageUpload;
}

declare module './pages/HomePage' {
  import { FC } from 'react';
  const HomePage: FC;
  export default HomePage;
}

declare module './pages/HistoryPage' {
  import { FC } from 'react';
  const HistoryPage: FC;
  export default HistoryPage;
}
import { AppBar, Toolbar, Typography, Button } from "@mui/material";
import { Link } from "react-router-dom";

export default function NavBar() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          食物营养分析
        </Typography>
        <Button color="inherit" component={Link} to="/">
          首页
        </Button>
        <Button color="inherit" component={Link} to="/upload">
          上传图片
        </Button>
        <Button color="inherit" component={Link} to="/history">
          历史记录
        </Button>
      </Toolbar>
    </AppBar>
  );
}
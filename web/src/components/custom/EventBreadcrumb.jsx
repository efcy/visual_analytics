import { useParams, Link } from "react-router-dom";
import { useSelector } from "react-redux";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import "@/styles/new.css";

const EventBreadcrumb = () => {
  const current_event = useSelector(
    (state) => state.breadcrumbReducer.current_event,
  );
  const current_game = useSelector(
    (state) => state.breadcrumbReducer.current_game,
  );
  return (
    <Breadcrumb className="ps-8">
      <BreadcrumbList>
        <BreadcrumbItem className="text-xl">
          <BreadcrumbLink asChild>
            <Link to="/">Events</Link>
          </BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbSeparator className="text-xl" />
        <BreadcrumbItem className="text-xl">
          <BreadcrumbLink>{current_event}</BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbSeparator className="text-xl" />
        <BreadcrumbItem className="text-xl">
          <BreadcrumbLink>{current_game}</BreadcrumbLink>
        </BreadcrumbItem>
      </BreadcrumbList>
    </Breadcrumb>
  );
};

export default EventBreadcrumb;

use shop_mongo;

// 1. Read: all Alice orders with computed total
db.orders.aggregate([
  {
    $lookup: {
      from: "users",
      localField: "user_id",
      foreignField: "_id",
      as: "user_info"
    }
  },
  { $unwind: "$user_info" },
  { $match: { "user_info.email": "alice@example.com" } },
  {
    $addFields: {
      total_amount: {
        $sum: {
          $map: {
            input: "$items",
            as: "item",
            in: { $multiply: ["$$item.quantity", "$$item.price"] }
          }
        }
      }
    }
  }
]);

// 2. Update: add discount for expensive orders
db.orders.aggregate([
  {
    $project: {
      total_amount: {
        $sum: {
          $map: {
            input: "$items",
            as: "item",
            in: { $multiply: ["$$item.quantity", "$$item.price"] }
          }
        }
      }
    }
  },
  { $match: { total_amount: { $gt: 80000 } } }
]).forEach(doc => {
  db.orders.updateOne({ _id: doc._id }, { $set: { discount: 10 } });
});

// 3. Delete: old cancelled orders
const cutoff = new Date();
cutoff.setDate(cutoff.getDate() - 30);
db.orders.deleteMany({ status: "cancelled", order_date: { $lt: cutoff } });

// 4. Aggregation by category
db.orders.aggregate([
  { $unwind: "$items" },
  {
    $lookup: {
      from: "products",
      localField: "items.product_id",
      foreignField: "_id",
      as: "product"
    }
  },
  { $unwind: "$product" },
  {
    $group: {
      _id: "$product.category",
      total_sold: { $sum: "$items.quantity" },
      total_revenue: { $sum: { $multiply: ["$items.quantity", "$items.price"] } }
    }
  },
  { $sort: { total_revenue: -1 } }
]);
